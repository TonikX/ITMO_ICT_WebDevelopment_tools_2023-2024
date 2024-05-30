from celery import Task
from celery.exceptions import MaxRetriesExceededError
from celery_worker import app
from ml import load_model, load_tokenizer, create_prediction_mask, predict_next_word
import httpx


BASE_WORDS_WHITELIST = ['вода', 'вода газированная', 'чай черный', 'кофе натуральный', 'молоко']  # leave empty to include all

OPTIONAL_WORDS_WHITELIST = ['арахис', 'грецкий орех', 'миндаль', 'ананас', 'киви', 'папайя', 'банан', 
                            'манго', 'лайм', 'лимон', 'грейпфрут', 'апельсин', 'мандарин', 'персик', 
                            'абрикос', 'яблоко', 'дыня', 'арбуз', 'клубника', 'малина', 'виноград', 
                            'черешня', 'брусника', 'вишня', 'ежевика', 'облепиха', 'черника', 'барбарис', 
                            'клюква', 'крыжовник', 'шиповник', 'шоколад молочный', 'мед', 'сливки',
                            'ваниль', 'гвоздика', 'имбирь', 'корица', 'краб', 'водоросли', 'икра красная', 
                            'сельдь', 'лосось', 'брокколи', 'шпинат', 'лук', 'горох', 'цуккини', 'помидор', 
                            'свекла', 'морковь', 'тыква', 'картофель', 'базилик', 'мята', 'хмель', 'укроп']


class PredictTask(Task):
    def __init__(self):
        super().__init__()
        self.tokenizer = None
        self.model = None
        self.base_mask = None
        self.optional_mask = None

    def __call__(self, *args, **kwargs):
        
        if not self.tokenizer: 
            self.tokenizer = load_tokenizer('models/tokenizer.pkl')
            if len(BASE_WORDS_WHITELIST):
                self.base_mask = create_prediction_mask(self.tokenizer, BASE_WORDS_WHITELIST)
            if len(OPTIONAL_WORDS_WHITELIST):
                self.optional_mask = create_prediction_mask(self.tokenizer, OPTIONAL_WORDS_WHITELIST)
                
        if not self.model:
            self.model = load_model('models/model.h5')
            
        return self.run(*args, **kwargs)


@app.task(ignore_result=False, bind=True, base=PredictTask)
def predict(self, ingredients_joined: str, url_to_send_results_to: str) -> dict[str]:
    try:
        if ingredients_joined == '':  # first ingredient is always base
            prediction = predict_next_word(self.tokenizer, self.model, ingredients_joined, mask=self.base_mask)
        else:
            prediction = predict_next_word(self.tokenizer, self.model, ingredients_joined, mask=self.optional_mask)
            
        if url_to_send_results_to != '':
            with httpx.Client() as client:
                client.post(f"{url_to_send_results_to}?ingredients_joined={ingredients_joined}&result={prediction}")

        return {'status': 'SUCCESS', 'result': prediction}
    except Exception as ex:
        try:
            self.retry(countdown=2)
        except MaxRetriesExceededError as ex:
            return {'status': 'FAIL', 'result': 'max retried achieved'}