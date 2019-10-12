from flask import Flask, request, render_template, url_for, redirect
import os, subprocess
import score
# import utils.(filename)

# To run this, type in terminal: `export FLASK_APP=main.py` (or whatever name of file is)
# Then type flask run
# Additional options: Use `flask run --host=0.0.0.0` or any other host you want to specify.
# additionally you can add `--port=4000` after the previous command to run on port 4000
app = Flask(__name__)

player1 = "Player 1"
player2 = "Player 2"
rounds = 0
current_round = 0
player1_score = 0
player2_score = 0

current_player = player1
turns = ['desc', 'guess']
turn = 0

current_desc = ""

# What to do when user goes to default route
@app.route('/')
def welcome(): # The function name can be anything

    # You can just return default text 
    # return "Hello. Welcome to default page"

    # You'd rather return a rendered html file
    return render_template("landing.html") 

@app.route('/gamesetup')
def game_setup():
    # RESET GLOBAL VARIABLES
    global player1, player2, player1_score, player2_score, rounds, current_round, current_player, current_desc
    player1 = "Player 1"
    player2 = "Player 2"
    rounds = 0
    current_round = 0
    player1_score = 0
    player2_score = 0
    current_player = player1
    current_desc = ""

    return render_template('gameops.html')

@app.route('/game',  methods=['POST'])
def eval_and_display():
    # If we come from GameOps, set our parameters accordingly
    
    print('p1', player1_score, 'p2', player2_score)

    if 'fromops' in request.form:
        global player1, player2, rounds
        if request.form['p1name']!="": player1 = request.form['p1name']
        if request.form['p2name']!="": player2 = request.form['p2name']
        current_player = player1
        rounds = int(request.form['numrounds'])*2
        # Display the player1 caption page
        return_page = "desc.html"
        return render_template(return_page, player=current_player)

    # If we come from desc, then we should generate image
    if 'from_desc' in request.form:
        caption = request.form['caption']
        global current_desc
        current_desc = caption
        # caption player is the one who provided caption to generate image
        caption_player = request.form['d_player']
        print(caption, caption_player)
        # next_player = player1 if caption_player==player2 else player2
        next_player = player2
        if caption_player==player2: next_player=player1

        # Generate image and copy to static folder
        FNULL=open(os.devnull, 'w')
        generator = subprocess.Popen(["bash", "generate_img.sh", caption], stdout=FNULL, stderr=FNULL)
        generator.wait()

        return render_template('guess.html', player=next_player)
    
    if 'from_prev' in request.form:
        
        prev_guesser= request.form['guesser']
        next_captioner = player1
        if prev_guesser == player2:
            next_captioner = player2
        # print(prev_guesser, next_captioner, player1_score, player2_score)
        return render_template("desc.html", player=next_captioner)

    # Read form and decide parameters, path and image

@app.route('/result', methods=['POST'])
def result_and_next():
    global current_round, player1_score, player2_score
    current_round+=1
    next_page=""
    if current_round == rounds:
        next_page="end"
    else:
        next_page="desc"

    guess = request.form['guessed']
    guesser = request.form['guesser']
    print("guesser", guesser)
    score_value = score.score_sentences(current_desc, guess)
    score_value = round(100*score_value, 2)
    print("score", score_value)
    if guesser == player1:
        player1_score += score_value
    else: player2_score += score_value

    print(current_round, current_desc)
    return render_template('result.html', 
    next_page=next_page, 
    score_val=score_value, 
    correct=current_desc, 
    guess=guess, 
    scoreof=guesser)


@app.route('/end', methods=['POST'])
def final_scoring():
    print(player1_score, player2_score)
    if player1_score>player2_score:
        winner=player1
    elif player2_score>player1_score:
        winner=player2
    else:
        winner="Nobody! It's a tie"
    return render_template("final.html", 
    player1=player1,
    player2=player2,
    player1_score=round(player1_score, 2), 
    player2_score=round(player2_score, 2), 
    winner=winner)