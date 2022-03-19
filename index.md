# shannotator
Self hosted bounding-box annotator tool. Built on a client-server model, this tool can be used to connect to multiple data backends, e.g. Azure Blob, GCBucket, S3 and even local storage on the server side and annotate them through a browser interface. Additionally it provides options to create separate projects, download individual and project level annotations etc.

Start by cloning the [repo](https://github.com/aiwabdn/shannotator).

# Installation

Make sure you have node version above `14.0.0`

```bash
cd shannotator/client
npm install
npm run serve
```

In a separate terminal
```bash
cd shannotator/server
conda create -n shannotator python=3.8
conda activate shannotator
pip install -r requirements.txt
uvicorn app:app --reload
```

Then visit `<<ip>>:8080` to visit the Shannotator Home page.
