# shannotator
self hosted annotator

# Installation

Make sure you have node version above `14.0.0`

```bash
cd client
npm install
npm run serve
```

In a separate terminal
```bash
cd shannotator/server
conda create -n shannotator python=3.8
conda activate shannotator
pip install -r requirements.txt
uvicorn app:app reload
```

Then visit `<<ip>>:8080` to visit the Shannotator Home page.
