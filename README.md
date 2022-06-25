# Для сборки и запуска приложения:

    docker-compose up -d --build

# Начать раунд: 

    http://127.0.0.1:1996/api/v1/roulette/start/

Необходимо передать имя пользователя, пример:

    {
        "user" : "Naruto"
    }

# Крутить рулетку:

    http://127.0.0.1:1996/api/v1/roulette/roll/

Необходимо передать в POST запросе пользователя:

    {
        "user" : "Naruto"
    }


# Закончить раунд 

    http://127.0.0.1:1996/api/v1/roulette/end/

PATCH запрос с именем пользователя:

    {
        "user" : "Naruto"
    }

# Cтатистика по раундам

    http://127.0.0.1:1996/api/v1/roulette/statistics/


# Статистика по пользователям

    http://127.0.0.1:1996/api/v1/roulette/statistics/?user_stat=1
