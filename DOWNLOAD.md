Dataset **ISIC Challenge 2018** can be downloaded in [Supervisely format](https://developer.supervisely.com/api-references/supervisely-annotation-json-format):

 [Download](https://assets.supervisely.com/remote/eyJsaW5rIjogImZzOi8vYXNzZXRzLzMzMTJfSVNJQyBDaGFsbGVuZ2UgMjAxOC9pc2ljLWNoYWxsZW5nZS0yMDE4LURhdGFzZXROaW5qYS50YXIiLCAic2lnIjogIkt4SERCdklETFRKRjBNTFJDcUIzM0JQTlVrT25RdFhxT01JZEVSQlkvWE09In0=)

As an alternative, it can be downloaded with *dataset-tools* package:
``` bash
pip install --upgrade dataset-tools
```

... using following python code:
``` python
import dataset_tools as dtools

dtools.download(dataset='ISIC Challenge 2018', dst_dir='~/dataset-ninja/')
```
Make sure not to overlook the [python code example](https://developer.supervisely.com/getting-started/python-sdk-tutorials/iterate-over-a-local-project) available on the Supervisely Developer Portal. It will give you a clear idea of how to effortlessly work with the downloaded dataset.

The data in original format can be [downloaded here](https://challenge.isic-archive.com/data/#2018).