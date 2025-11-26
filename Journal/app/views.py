#FILE ATTUALE CON VECCHIO SISTEMA REDIS


from django.shortcuts import render, redirect
from .models import Post
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import NewUserForm, PostForm
from django.template import RequestContext
import json
import hashlib
from web3 import Web3
import random
import redis
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# CONFIG FOR REDIS SERVER
SERVER_IP = os.getenv('REDIS_HOST', '127.0.0.1')
SERVER_PORT = os.getenv('REDIS_PORT', '6379')
PASSWORD = os.getenv('REDIS_PASSWORD', '')
DB = int(os.getenv('REDIS_DB', '0'))

#ALL POST
def journal(request):
    post = Post.objects.all()
    return render(request, 'app/index.html', {'journal': post})

#REGISTRATION
def register_request(request):
	if request.method == "POST":
        
		form = NewUserForm(request.POST)
		post_journal = Post.objects.all()
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect("journal")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render (request=request, template_name="app/register.html", context={"register_form":form})
    #valutare se inviare ad una pagina di registrazione completata

#LOGIN
def login_request(request):


	warning = None
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			
			#REDIS
			#r = redis.Redis(host='127.0.0.1', port=6379, db=0)
			client = redis.Redis(host=SERVER_IP, 
                                port=int(SERVER_PORT), 
                                password=PASSWORD if PASSWORD else None,
                                db=DB,
                                decode_responses=True)
			if user is not None:
				login(request, user)
				form_post = PostForm()
				#REDIS
				if user.is_staff: 
					last_ip = client.get(f'{user.username}:last_ip')
					current_ip = request.META['REMOTE_ADDR']
					if last_ip is not None and last_ip != current_ip:
						warning = 'Il tuo ultimo accesso è stato effettuato da un indirizzo IP diverso. Assicurati che questo sia il tuo accesso!'
					else:
						warning = 'Ben tornato!'
						client.set(f'{user.username}:last_ip', current_ip)   
        			
					#return render(request , 'degree/add_student.html' , {'warning': warning})
						#return render(request, 'app/blog_post.html', {'warning': warning, 'form': form_post})
						return render(request, 'app/blog_post.html', {"warning":warning, 'form': form_post})
						

				else:
					#return redirect('blogpost') 
					return render(request, 'app/blog_post.html', {"warning":'Ben tornato!11111', 'form': form_post})
				#####
				#messages.info(request, f"You are now logged in as {username}.")
				#messag_succes = "You are now logged {}".format(username)
				#return render(request, "app/blog_post.html", {'form': PostForm()})
				
				#return render(request, 'app/blog_post.html', {"warning":'Ben tornato!22222', 'form': form_post})
				#response = redirect('blogpost')
				#return response
			else:
				return render(request, "app/login.html", {"error":'Invalid username or password', "login_form":form})
		else:
			#messages.error(request,"Invalid username or password.")
			return render(request, "app/login.html", {"error":'Invalid username or password', "login_form":form})
	form = AuthenticationForm()
	return render(request=request, template_name="app/login.html", context={"login_form":form})



#CREATE POST
def blogpost_request(request):
	if request.method == "POST":

		form_post = PostForm(request.POST)

		if form_post.is_valid():
			post = form_post.save(commit=False)
			post.author = request.user
			author = str(post.author)
			post_serializable = str(post)

			try:
				w3 = Web3(Web3.HTTPProvider(os.getenv('ETH_NETWORK_URL')))
				privateKey = os.getenv('ETH_PRIVATE_KEY')
				address = os.getenv('ETH_ADDRESS')
						
				nonce = w3.eth.get_transaction_count(address)
				gasPrice = w3.eth.gas_price
				value = w3.to_wei(0, 'ether')
				signedTx = w3.eth.account.sign_transaction(dict(
					nonce = nonce,
					gasPrice = gasPrice,
					gas = int(os.getenv('GAS_LIMIT', '21000')),
					to = '0x0000000000000000000000000000000000000000',
					value = value,
					data = hashlib.sha256(json.dumps({
						'Post': {
							'name': author,
							'post_data': post_serializable,
						},
					}).encode('utf-8')).hexdigest()
				), privateKey)

				tx = w3.eth.send_raw_transaction(signedTx[0])
				txId = w3.to_hex(tx)

				characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
				identifier = ''

				for i in range(10):
					identifier += random.choice(characters)

				post.txId = txId
				post.identifier = identifier
			except Exception as e:
				print(f"Blockchain error: {e}")
				post.txId = None
				post.identifier = None
			
			post.save()
			return render(request, "app/blog_post.html", {"success":'Your post is correctly inserted', 'form': PostForm()})
		else:
			return render(request, 'app/blog_post.html', {'form': form_post, 'error': f'Form errors: {form_post.errors}'})

	else:
		form_post = PostForm()
		return render(request, 'app/blog_post.html', {'form': form_post})


#SEARCH POST
def search_post(request):
    return render(request , 'app/search_post.html')


#DETAILS POST
def post_details(request, id):
    try:
        post = Post.objects.get(id=id)
    except Post.DoesNotExist:
        messages.error(request, 'Articolo non trovato')
        return redirect('journal')
    return render(request, 'app/post_details.html', {'post': post}) 



def is_admin(user):
  return user.is_staff  


def custom_logout(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("journal")