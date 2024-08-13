# Load testing metrics API

If you have any questions, you can ask [@Nikita Filonov](https://t.me/sound_right)

## Project setup
```shell
git clone https://github.com/Nikita-Filonov/load-testing-hub-api.git
cd load-testing-hub-api

pip install -r requirements.txt
uvicorn main:app --reload
```

## Apply migrations
```shell
alemibc upgrade head
```