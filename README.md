A web application for translating srt subtitles from one language to another. It has its own API
Install: pip install -r requirements.txt
Run: uvicorn main:app --reload
Deploy commands: invoke basic-deploy -a <admin_name> -p <password> (to make a deployment)
                 invoke add-user -a <admin_name> -p <password> (to add user)
