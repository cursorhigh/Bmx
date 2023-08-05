import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer,WebsocketConsumer
from django.core.cache import cache
import json
import random
import os
import time
import redis
redis_client = redis.from_url('redis location')
class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.pid = self.scope['url_route']['kwargs']['playerid']
        self.room_name = self.scope['url_route']['kwargs']['roomname']
        self.playername = self.scope['url_route']['kwargs']['playername']
        self.oname = self.scope['url_route']['kwargs']['oname']
        self.room_group_name = self.room_name
        player_name = self.room_name.split('_')[0]
        self.unbind = self.room_name.split('_')
        self.unbind.remove(self.room_name.split('_')[-1])
        self.title = self.room_name.split('_')[-1]
        self.seed_value = random.randint(1, 10000)
        cache.set(self.pid, True, timeout=180)
        for x in self.unbind:
            if self.pid != x:
                self.oid = x
            else:
                pass
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        times = 0
        if times == 0:
            await asyncio.sleep(5)
        while times <= 23:
            if await self.search_in_cache(self.oid):
                await self.notify_opponent('opponent_connected')
                await self.send_opponent_id(self.oname,self.title)
                break
            else:
                await asyncio.sleep(5)
                times += 1
        if times == 6:
            cache.delete(self.pid)
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )
            message = 'Opponent left. Redirecting to the homepage...'
            response = {
                'type': 'notify_disconnection',
                'message': message
            }
            await self.send(text_data=json.dumps(response))
        if self.title == 'Math':
            file_path = os.path.join('static', 'questions', 'math', 'math.json')
        elif self.title == 'Olympics':
            file_path = os.path.join('static', 'questions', 'olympics', 'olympics.json')
        elif self.title == 'IPL':
            file_path = os.path.join('static', 'questions', 'ipl', 'ipl.json')
        elif self.title == 'Computer':
            file_path = os.path.join('static', 'questions', 'computer', 'computer.json')
        elif self.title == 'FIFA':
            file_path = os.path.join('static', 'questions', 'fifa', 'fifa.json')
        elif self.title == 'Mythology':
            file_path = os.path.join('static', 'questions', 'mythology', 'mythology.json')
        with open(file_path,'r') as f:
            self.questions_list = json.load(f)
        if self.pid==player_name:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'send_seed',
                    'player_name': player_name,
                    'seed_value': self.seed_value
                }
            )
        self.current_question_index = 0
        self.player_score=0
        self.skipleft=5
        self.totalq=1
        self.oppnentscore=0

    async def send_seed(self, event):
        self.seed_value = event['seed_value']
        random.seed(self.seed_value)
        random.shuffle(self.questions_list)
        self.questions_list = self.questions_list[:15]
        self.answers_list = [question['correct_answer'] for question in self.questions_list]

    async def disconnect(self, close_code):
        winnerid=self.oid
        winnerscore=self.oppnentscore
        youid=self.pid
        youscore=self.player_score
        cache.delete(self.pid)
        cache.delete(f'{self.oid}_done')
        message = {
            'type': 'player_left',
            'message': 'Your opponent has left the game. Redirecting to the homepage...',
            'winnerid': winnerid,
            'winnerscore': winnerscore,
            'youid':youid,
            'youscore':youscore
        }
        await self.channel_layer.group_send(self.room_group_name, message)
        await self.channel_layer.group_discard(self.room_group_name,self.channel_name)

    async def send_opponent_id(self, opponent_id,title):
            await self.send(json.dumps({
                'type': 'opponent_id',
                'opponent_id': opponent_id,
                'title':title
            }))

    async def receive(self, text_data):
        data = json.loads(text_data)
        if data['type'] == 'submit_answer':
            selected_option = data['option']
            self.totalq+=1
            if selected_option == self.answers_list[self.current_question_index-1]:
                self.player_score += 10
                await self.update_player_score(self.player_score)
                message={
                    'type': 'send.score',
                    'opponent_score': self.player_score,
                    'bywho':self.pid
                }
                await self.channel_layer.group_send(self.room_group_name, message)
            else:
                if self.totalq<=10:
                    await self.send_question()
                else:
                    await self.gamerover()

        elif data['type'] == 'request_question':
            if self.totalq<=10:
                await self.send_question()
            else:
                await self.gamerover()
        elif data['type'] == 'player_surrender':
            await self.surrenderup()

        elif data['type'] == 'player_skip':
            if self.skipleft>=1:
                if self.player_score>0:
                    self.player_score -=5
                await self.update_player_score(self.player_score)
                message={
                    'type': 'send.score',
                    'opponent_score': self.player_score,
                    'bywho':self.pid
                }
                await self.channel_layer.group_send(self.room_group_name, message)

    async def send_score(self,event):
        if event['bywho']!=self.pid:
            cache.delete(self.pid)
            opponent_score = event['opponent_score'] 
            self.oppnentscore=opponent_score
            await self.send(text_data=json.dumps({
                'type': 'send.score',
                'opponent_score': opponent_score
            }))      

    async def giveup_now(self,event):
        if event['bywho']!=self.pid:
            response= {
                    'type':'giveup',
                    'bywho':event['bywho']            
                }
            await self.send(text_data=json.dumps(response))

    async def send_question(self):
        if self.current_question_index < len(self.questions_list):
            current_question = self.questions_list[self.current_question_index]
            self.current_question_index += 1
            print(self.current_question_index)
            options = current_question['options']
            random.shuffle(options)
            message = {
                'type': 'question',
                'question': current_question['question'],
                'options': options,
            }
            await self.send(text_data=json.dumps(message))
        else:
            await self.gamerover()

    async def update_player_score(self, player_score):
        response = {
            'type': 'update_player_score',
            'player_score': player_score
        }
        await self.send(text_data=json.dumps(response))

    async def player_left(self, event):
        cache.delete(f'{self.oid}_done')
        await self.send(text_data=json.dumps(event))

    async def search_in_cache(self, data):
        result = cache.get(data)
        return result is not None

    async def notify_opponent(self, type):
        message = {
            'type': type
        }
        await self.send(text_data=json.dumps(message))

    async def surrenderup(self):
        winnerid=self.oid
        winnerscore=self.oppnentscore
        youid=self.pid
        youscore=self.player_score
        response= {
            'type':'giveup.now',
            'bywho':youid            
        }
        await self.channel_layer.group_send(self.room_group_name, response)
        message = {
                'type': 'surrenderup',
                'winnerid': winnerid,
                'winnerscore': winnerscore,
                'youid':youid,
                'youscore':youscore
            }
        await self.send(text_data=json.dumps(message))

    async def gamerover(self):
        await self.send(text_data=json.dumps({'type': 'game_over'}))
        cache.set(f'{self.pid}_done', {'done': True, 'score':self.player_score}, timeout=180)
        opponent_pid = self.oid
        while True:
            opponent_done = cache.get(f'{opponent_pid}_done')
            if opponent_done and opponent_done['done']:
                player1_score = self.player_score
                opponent_score = opponent_done['score']
                if player1_score > opponent_score:
                    winner = f'{self.pid},you won the game! yeah'
                    prompt = f'{self.playername},you won the game! yeah'
                elif player1_score < opponent_score:
                    winner = f'{opponent_pid},opponent won the game'
                    prompt = f'{self.oname},opponent won the game'
                else:
                    winner = "It's a tie! Baby"
                    prompt = "It's a tie! Baby"
                cache.delete(f'{opponent_pid}_done')
                message = {
                    'type': 'game_results',
                    'winner': winner,
                    'prompt':prompt,
                    'player1_id': self.pid,
                    'player1_name':self.playername,
                    'player1_score': player1_score,
                    'player2_id': opponent_pid,
                    'player2_name': self.oname,
                    'player2_score': opponent_score
                }
                await self.send(text_data=json.dumps(message))
                break  
            await asyncio.sleep(2)

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.username = self.scope['url_route']['kwargs']['username']
        await self.channel_layer.group_add(
            "globalroom",
            self.channel_name
        )
        await self.accept()
        chat_history = get_chat_history_from_redis()

        # Send the chat history to the user
        for message_data in chat_history:
            message = message_data['message']
            username = message_data['username']
            await self.send(text_data=json.dumps({
                'type': 'chat_history',
                'message': message,
                'username': username,
            }))

    async def disconnect(self, close_code):
        # Remove the user from the global chat group
        await self.channel_layer.group_discard(
            "globalroom",
            self.channel_name
        )

    async def receive(self, text_data):
        message_data = json.loads(text_data)
        message = message_data['message']
        save_message_to_redis(message, self.username)
        await self.channel_layer.group_send(
            "globalroom",
            {
                'type': 'chat.message',
                'message': message,
                'username': self.username,  # Include the username in the response
            }
        )

    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        if username!= self.username:
            await self.send(text_data=json.dumps({
                'message': message,
                'username': username,
            }))

def save_message_to_redis(message, username):
    timestamp = int(time.time())
    key = f"message:{timestamp}"
    data = {
        'message': message,
        'username': username,
        'timestamp': timestamp,
    }
    redis_client.setex(key, 86400, json.dumps(data))

def get_chat_history_from_redis():
    keys = redis_client.keys("message:*")
    chat_history = []

    for key in keys:
        data = redis_client.get(key)
        if data:
            chat_history.append(json.loads(data))

    chat_history.sort(key=lambda x: int(x['timestamp']))

    return chat_history
