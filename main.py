from bucket import create_bucket, delete_bucket, return_bucket_object
from blob import upload_blob, delete_blob, download_blob, list_blobs
from vision import detect_pdf_text
from process_json import create_dataframe
from predict import make_prediction_mlauto
from text_to_speech import get_text_for_speech, make_speech_for_batch, merge_batch_audios
import time
import os


def main(path_for_pdf, project_id, model_display_name, language_code, voice_name, path_for_csv='./'):
    # create buckets
    bucket_name_pdf = '{}-pdf'.format(project_id)
    create_bucket(bucket_name_pdf)
    bucket_name_json = '{}-json'.format(project_id)
    create_bucket(bucket_name_json)
    bucket_name_prediction = '{}-prediction'.format(project_id)
    create_bucket(bucket_name_prediction)
    bucket_name_mp3 = '{}-mp3'.format(project_id)
    create_bucket(bucket_name_mp3)
    time.sleep(1)
    bucket_mp3 = return_bucket_object(bucket_name_mp3)
    # upload pdf
    pdf_blob_name = path_for_pdf.split('/')[-1]
    upload_blob(bucket_name_pdf, path_for_pdf, pdf_blob_name)
    time.sleep(1)
    # request vision API
    gcs_source_uri = 'gs://{}/{}'.format(bucket_name_pdf, pdf_blob_name)
    gcs_destination_uri = 'gs://{}/{}'.format(
        bucket_name_json, pdf_blob_name.rstrip('.pdf'))
    json_blob_list = detect_pdf_text(gcs_source_uri, gcs_destination_uri)
    time.sleep(1)
    # create dataframe and make predictions
    #pdf_id = pdf_blob_name.replace(".pdf", "")[:8]
    for json_blob in json_blob_list:
        df = create_dataframe(json_blob)
        gcs_output_uri = 'gs://{}/{}'.format(
            bucket_name_prediction, json_blob.name.rstrip('.json'))
        make_prediction_mlauto(df, model_display_name,
                               gcs_output_uri, project_id)
        json_blob.delete()
        #df = make_prediction_scikilearn(df)
        #path = './{}.csv'.format(json_blob.name.rstrip('.json'))
        #df.to_csv(path, index=False)
        # delete csv
    # download predicted csv
    predicted_blobs = list_blobs(bucket_name_prediction)
    batch_audio_segments = []
    for predicted_blob in predicted_blobs:
        if predicted_blob.name.split('/')[-1].startswith('tables'):
            predicted_blob.download_to_filename('{}{}_{}'.format(
                path_for_csv, predicted_blob.name.split('/')[0], predicted_blob.name.split('/')[-1]))
            time.sleep(1)
            # make speech
            text_list = get_text_for_speech('{}{}_{}'.format(
                path_for_csv, predicted_blob.name.split('/')[0], predicted_blob.name.split('/')[-1]))
            batch_name = predicted_blob.name.split('/')[0]
            batch_audio_segment = make_speech_for_batch(text_list, language_code, voice_name,
                                                        batch_name, bucket_mp3)
            batch_audio_segments.append(batch_audio_segment)
            # remove csv
            os.remove('{}{}_{}'.format(
                path_for_csv, predicted_blob.name.split('/')[0], predicted_blob.name.split('/')[-1]))
        predicted_blob.delete()

    # merge audios and save file
    path_for_audio = '{}.mp3'.format(pdf_blob_name)
    merge_batch_audios(batch_audio_segments, path_for_audio)

    # delete json files from GCP
    # for json_blob in json_blob_list:
    #    json_blob.delete()
    # delete pdf from GCP
    delete_blob(bucket_name_pdf, pdf_blob_name)
    time.sleep(1)
    # delete buckets
    delete_bucket(bucket_name_json)
    delete_bucket(bucket_name_pdf)
    delete_bucket(bucket_name_prediction)
    delete_bucket(bucket_name_mp3)


if __name__ == "__main__":
    path_for_pdf = './pdf/The-4-Hour-Work-Week.pdf'
    project_id = 'audiobook-maker-297701'
    model_display_name = 'modelo_1_16075452_20201209022505'
    language_code = 'en-US'
    voice_name = 'en-US-Wavenet-F'
    main(path_for_pdf, project_id, model_display_name, language_code, voice_name)
