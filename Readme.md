*** Webapp für Zivilgesellschaft und gute Diskussionskultur auf Twitter ***

Zwei Apps in der Mache:
- "login" organizes Twitter Login
- "block" allows you to install all kinds of blocklists

TODO login:
- give the app some nice design

TODO block:
- blocking is currently implemented in a way that will probably kill the server if too many people do it. should be implemented with a scheduler and recurrent jobs for blocking.
- blocklist models and import export functionality
- auto update blocklists with retweeters from certain hate-accounts (e.g. new right)

For running requires the following values in the Environment:
os.environ['APP_KEY']
os.environ['APP_SECRET']
os.environ["DEBUG"] = "enabled" #Optional
os.environ["SECRET_KEY"]
os.environ["DB_Name"]
os.environ['DB_USER']
os.environ['DB_PASSWORD']
os.environ['DB_HOST']
