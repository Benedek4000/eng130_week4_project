# Website project

Welcome to eng130 website project. In this short introduction, we will inform you on how to get the website integrated in your system with simple steps (as long as our public server is running). <br/>
### All you need

The list of requirements needed for this website is listed in requirements.txt, all you need to do is clone this repository into your local machine and `cd eng130_week4_project` to get into the folder. After that is done, run the installation by writing in the command line

```bash
pip install -r requirements.txt
```

Once all is installed, export the following and run the app.py by either doing it through vscode or any other software or writing in the command line:

```bash
export BUCKET=eng130-videos
export aws_access_key_id=YOUR_KEY
export aws_secret_key=YOUR_SECRET_KEY

python app.py
```
