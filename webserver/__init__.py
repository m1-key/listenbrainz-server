from flask import Flask
import sys
import os

_kafka = None


def create_app():
    global _kafka

    app = Flask(__name__)

    # Configuration
    sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), ".."))
    sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), "../listenstore"))
    import config
    app.config.from_object(config)

    # Logging
    from webserver.loggers import init_loggers
    init_loggers(app)

    # Kafka connection
    from kafka_connection import init_kafka_connection
    init_kafka_connection(app.config['KAFKA_CONNECT'])

    # Cassandra connection
    from cassandra_connection import init_cassandra_connection
    init_cassandra_connection(app.config['CASSANDRA_SERVER'], app.config['CASSANDRA_KEYSPACE'])

    # Database connection
    from db import init_db_connection
    init_db_connection(app.config['PG_CONNECT'])

    # Memcached
#    if 'MEMCACHED_SERVERS' in app.config:
#        from db import cache
#        cache.init(app.config['MEMCACHED_SERVERS'],
#                   app.config['MEMCACHED_NAMESPACE'],
#                   debug=1 if app.debug else 0)

    # OAuth
    from webserver.login import login_manager, provider
    login_manager.init_app(app)
    provider.init(app.config['MUSICBRAINZ_CLIENT_ID'],
                  app.config['MUSICBRAINZ_CLIENT_SECRET'])

    # Error handling
    from webserver.errors import init_error_handlers
    init_error_handlers(app)

    # Template utilities
    app.jinja_env.add_extension('jinja2.ext.do')
    from webserver import utils
    app.jinja_env.filters['date'] = utils.reformat_date
    app.jinja_env.filters['datetime'] = utils.reformat_datetime

    # Blueprints
    from webserver.views.index import index_bp
    from webserver.views.login import login_bp
    from webserver.views.api import api_bp
    from webserver.views.user import user_bp
    app.register_blueprint(index_bp)
    app.register_blueprint(login_bp, url_prefix='/login')
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(api_bp)

    return app