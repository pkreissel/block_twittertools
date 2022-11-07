# Webapp für Zivilgesellschaft und gute Diskussionskultur auf Twitter

Zwei Apps in der Mache:

* "login" organizes Twitter Login
* "block" allows you to install all kinds of blocklists

These Apps are based on the Django Python Web-Framework. There are two apps, login and block. Website rendering is controlled in the respective "view.py" functions. Database modeling is done in models.py. Here is more info on Django: https://www.djangoproject.com

**TODO login:**

* [ ] give the app some nice design

**TODO block:**

* [ ] blocking is currently implemented in a way that will probably kill the server if too many people do it. should be implemented with a scheduler and recurrent jobs for blocking.
* [ ] blocklist models and import export functionality
* [ ] auto update blocklists with retweeters from certain hate-accounts (e.g. new right)

*For running requires the following values in the Environment:*

* os.environ['APP_KEY']
* os.environ['APP_SECRET']
* os.environ["DEBUG"] = "disabled" / "enabled"
* os.environ["SECRET_KEY"]
* os.environ["DB_Name"]
* os.environ['DB_USER']
* os.environ['DB_PASSWORD']
* os.environ['DB_HOST']
* os.environ['ROOT_PROD'] = "https://production.server.com"
* os.environ['ROOT_TEST'] = "http://test.server.com:8000"

**App-Ideas:**

* Send Love to random far right accounts
* Dashboard for monitoring of a list of far right accounts
