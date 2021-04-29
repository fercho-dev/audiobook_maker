# audiobook_maker

Transform your PDFs into mp3 files.

### How does it work?

For this project I use Google Cloud services to convert the PDFs. Specifically, [Vision AI](https://cloud.google.com/vision/?utm_source=google&utm_medium=cpc&utm_campaign=latam-MX-all-es-dr-BKWS-all-all-trial-b-dr-1009897-LUAC0009343&utm_content=text-ad-none-any-DEV_c-CRE_346469506971-ADGP_Hybrid%20%7C%20BKWS%20-%20MIX%20%7C%20Txt%20~%20Machine%20Learning_Cloud%20Vision%20API-KWID_43700046044601528-kwd-616019569584&utm_term=KW_%2Bgoogle%20%2Bvision-ST_%2BGoogle%20%2BVision&gclid=CjwKCAjwj6SEBhAOEiwAvFRuKOra6CmX-zV_H3l55_KazecRSDwXbv7FLCIm9vAkG0Yc_1uxxQfguRoCGgwQAvD_BwE&gclsrc=aw.ds), [Text-to-Speech](https://cloud.google.com/text-to-speech), [AutoML Tables](https://cloud.google.com/automl-tables) and [Cloud Storage](https://cloud.google.com/storage/?utm_source=google&utm_medium=cpc&utm_campaign=latam-MX-all-es-dr-BKWS-all-all-trial-e-dr-1009897-LUAC0009347&utm_content=text-ad-none-any-DEV_c-CRE_386296505483-ADGP_Hybrid%20%7C%20BKWS%20-%20MIX%20%7C%20Txt%20~%20Storage_Cloud%20Storage-KWID_43700043800324493-kwd-308056723381&utm_term=KW_google%20cloud%20storage-ST_Google%20Cloud%20Storage&gclid=CjwKCAjwj6SEBhAOEiwAvFRuKNKv7sLjUYajuELFkUN7MpU9tEkZADFJZG279JCOMKrIJWyz3D_kExoCgzcQAvD_BwE&gclsrc=aw.ds)

Broadly speaking, the process can be divided in three steps:

- Extract the text from the pdf.

When you run the _main.py_ file you must give the path to the pdf you want to transform. This pdf will be send to Cloud Storage. Then, Vision AI will extract the text and return it in a json file.

- Process the json and create a string with the relevant text.

The json file will include text that may not be important for an mp3, such as the page number. To classify which text should be included in the audio file and which not, I used an AutoML Tables model. To train the model I created my own dataset. I label about 1000 examples. This dataset is not included in this repository. You must create your own.

- Convert the string to audio and save an mp3 file.

Text-to-Speech transforms strings into audio, but can't procces strings with more than 5000 characters. So, we do it in a loop and create various segments of audio. To manipulate these segments and join them into one I used [pydub](https://pypi.org/project/pydub/) library.

### What you need to do

You can't just run the _main.py_ file and expect it to work. You need to do some previous tasks.

- Create a google cloud project.
- Enable the necessary APIs: Vision AI, Text-to-Speech, Cloud Storage, AutoML Tables.
- Create a dataset to train the AutoML Tables model

Once you have this, go to the bottom of _main.py_ file and add the 5 variables needed: path_for_pdf, project_id, model_display_name from AutoML Tables and languaje_code and voice_name from Text-to-Speech.
