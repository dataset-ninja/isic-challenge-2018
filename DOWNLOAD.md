Dataset **ISIC Challenge 2018** can be downloaded in [Supervisely format](https://developer.supervisely.com/api-references/supervisely-annotation-json-format):

 [Download](https://assets.supervisely.com/remote/eyJsaW5rIjogInMzOi8vc3VwZXJ2aXNlbHktZGF0YXNldHMvMzMxMl9JU0lDIENoYWxsZW5nZSAyMDE4L2lzaWMtY2hhbGxlbmdlLTIwMTgtRGF0YXNldE5pbmphLnRhciIsICJzaWciOiAiRW9JUTh5Wm91RXNTV243RmpLbDFUVHlHSHp0ZzNoRzZDODFIZ0RFYjlSST0ifQ==?response-content-disposition=attachment%3B%20filename%3D%22isic-challenge-2018-DatasetNinja.tar%22)

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