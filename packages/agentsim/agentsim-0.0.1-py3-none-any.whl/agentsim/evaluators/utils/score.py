import asyncio

# this object contains a single score
# the score can be of any type, including a list of scores
class Score(object):
    def __init__(self, score, result, scorer_args=None):
        self.score = score
        self.result = result
        self.scorer_args = scorer_args

    def __repr__(self):
        return f'{self.score}'

# scorer decorator to wrap an app scorer inside a Score object
def scorer(score_func):
    def wrapper(*scorer_args):
        # Check if the score function is async
        if asyncio.iscoroutinefunction(score_func):
            # If score_func is async, return a Future Score object
            async def async_wrapper():
                score = await score_func(*scorer_args)
                return Score(score, scorer_args)
            return async_wrapper()
        else:
            # If score_func is sync, return a Score object
            score, result = score_func(*scorer_args)
            return Score(score, result, scorer_args)
    return wrapper

