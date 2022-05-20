# GitRemoteRunner

VScode launch.json helper for uploading and running code on a remote Debian host via github and SSH.

Change launch.json "program" key to 

{
    "configurations": [
        {
            ...
            "program": "${workspaceFolder}/pusher.py",
            ...
        }
    ]
}
