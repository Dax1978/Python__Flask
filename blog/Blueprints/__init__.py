from flask import Flask

def register_blueprints(app: Flask):
    from blog.Blueprints import admin
    from blog.Blueprints.api.views import api_blueprint
    from blog.Blueprints.auth.views import auth
    from blog.Blueprints.user.views import user
    from blog.Blueprints.author.views import author
    from blog.Blueprints.article.views import article


    app.register_blueprint(user)
    app.register_blueprint(auth)
    app.register_blueprint(author)
    app.register_blueprint(article)
    app.register_blueprint(api_blueprint)

    admin.register_views()