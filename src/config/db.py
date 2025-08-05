TORTOISE_ORM = {
    "connections": {
        "default": "sqlite://database.db"
    },
    "apps": {
        "models": {
            "models": [
                "src.database.models",
                "aerich.models"
            ],
            "default_connection": "default"
        }
    }
}