var form = document.getElementById('userInfo');
var username = document.getElementById('name');
var button = document.getElementById('start');
var team1 = document.getElementById('t1');
var team2 = document.getElementById('t2');
var info = document.getElementById('infoUpdate');
var calls = document.getElementById('userHands');

var socket = io.connect('http://localhost:5000');
var players;
var finalName;
var finalTeam;
var teamChoice;
var raise = 0;
var cut;
var hand;      // hand is array with deck[0] and indices of hand[1]
var colors = ['yellow', 'purple'];
var position;
var notFirst = false;
var suitRound;

socket.on('teamUpdate', function(players) {
   var tm1 = document.getElementById('team1');
   var tm2 = document.getElementById('team2');
   var totalHTML = tm1.innerHTML + tm2.innerHTML;

   totalHTML = totalHTML.replace('<h2>Team 1</h2>', '');
   totalHTML = totalHTML.replace('<h2>Team 2</h2>', '');

   for (let i = 0; i < players.length; i++) {
      var player = players[i];

      if (!totalHTML.includes(player['username'])) {
         var html = '<li>' + player['username'] + '</li>';

         if (player['team'] == 1) {
            tm2.innerHTML += html;
         }

         else {
            tm1.innerHTML += html;
         }
      }
   }
});


// lets client know game is about to start
// click event on start button at bottom of form
button.addEventListener('click', function() {
   console.log(team1.checked, team2.checked);

   if (username.value != undefined && (team1.checked == true || team2.checked == true)) {
      finalName = username.value;

      // check which radio button is checked
      if (team1.checked)
         teamChoice = team1.value;
      else if (team2.checked)
         teamChoice = team2.value;

      // check that form is not empty
      if (finalName != '' && teamChoice != '') {
         button.innerHTML = 'Wating for Players';
         socket.emit('waiting', {
            'socketName': finalName,
            'teamChoice': teamChoice
         });

         button.style.pointerEvents = 'none';
      }
      
      // listen for events
      socket.on('start', function(data) {
         players = data;
         form.style.display = 'none';
         document.getElementById('teamList').style.display = 'none';

         // check to see team of client
         for (let i = 0; i < players.length; i++) {
            if (finalName == players[i]['username']) {
               finalTeam = players[i]['team'];
            }
         }

         // deal cards and hand
         fancyAnimations();
         hand = showHand(players);

         // let server know to start call function
         // timeout function to wait for animations to finish
         setTimeout(function() {
            document.getElementById('numHands').style.display = 'flex';
            socket.emit('startCall', 1);

            // remove previous information of who joined what team
            var tm1 = document.getElementById('team1');
            var tm2 = document.getElementById('team2');
            tm1.innerHTML = '<h2>Team 1</h2>'
            tm2.innerHTML = '<h2>Team 2</h2>'
            document.getElementById('teamList').style.display = 'flex';

         }, 8000);
         
      });
   }
});

socket.on('signalCall', function(data) {
   var choice = data[0];
   var name = data[1];
   
   // choice == 2 -> used for raising
   if (choice == 2) {
      // change indicator label
      info.innerHTML = 'Would you like to raise?';
      
      // allow button to click
      calls.style.pointerEvents = 'auto';
   }

   // choice == 1 -> turn to call
   else if (choice == 1) {
      info.innerHTML = 'Your Turn to Call';
      calls.style.pointerEvents = 'auto';
   }
   else {
      info.innerHTML = 'Waiting for ' + name + ' to call';
      calls.style.pointerEvents = 'none';
   }
});

// click event for call button
calls.addEventListener('click', function() {
   let hands = document.getElementById('handVal').value;

   if (hands != undefined && hands >= 0 && hands <= 8 && hands != 1 && hands != 2 && hands != 3 && hands != 4 && hands != 5) {
      calls.style.pointerEvents = 'none';

      // send value to to server
      socket.emit('call', {
         'username': finalName,
         'numCalls': hands
      });
   }
});

// add call information to webpage
socket.on('updateCall', function(player) {

   var tm1 = document.getElementById('team1');
   var tm2 = document.getElementById('team2');
   
   var html = '<li>' + player['username'] + ': ' + player['handsCalled'] + ' hands</li>';

   // check for raising
   if (raise == 1) {
      var checkString = '<li>' + player['username'] + ': ';
      
      if (tm1.innerHTML.includes(checkString)) {
         let start = tm1.innerHTML.indexOf(checkString);

         // +5 to include the </li> tag
         let end = tm1.innerHTML.indexOf('</li>', start) + 5;

         let oldHTML = tm1.innerHTML.slice(start, end);
         tm1.innerHTML = tm1.innerHTML.replace(oldHTML, html);
         // console.log(oldHTML);
         // console.log(start, end);
      }

      else if (tm2.innerHTML.includes(checkString)) {
         let start = tm2.innerHTML.indexOf(checkString);
         let end = tm2.innerHTML.indexOf('</li>', start) + 5;

         let oldHTML = tm2.innerHTML.slice(start, end);
         tm2.innerHTML = tm2.innerHTML.replace(oldHTML, html);
         // console.log(oldHTML);
         // console.log(start, end);
      }
   }

   // initial calling
   else if (raise == 0) {

      // update team 0
      if (player['team'] == 0) {
         tm1.innerHTML += html;
      }

      // update team 1
      else {
         tm2.innerHTML += html;
      }
   }

   // next player caller
   if (raise == 1) {
      socket.emit('raiseCall');
   }
   
   else if (raise == 0) {
      socket.emit('startCall', 0);
   }

});

// option to raise
socket.on('raiseCalls', function() {
   raise = 1;

   // restart calling procedure
   socket.emit('raiseCall');

});

socket.on('finishCall', function() {
   // remove header, teamList, and form (numHands)
   // document.getElementById('header').style.display = 'none';
   info.innerHTML = '';
   document.getElementById('teamList').style.display = 'none';
   document.getElementById('numHands').style.display = 'none';

   // stops calling socket functions
   raise = 2;
});

socket.on('cut', function(player) {
   // show form to selected user
   if (player['username'] == finalName) {
      var cutForm = document.getElementById('cut');
      
      info.innerHTML = 'What is Cut?';
      cutForm.style.display = 'flex';

      // get document element for call event
      var choices = document.getElementsByClassName('cutChoice');

      // serach choices for value
      for (let i = 0; i < choices.length; i++) {

         // add event listener to each button
         choices[i].addEventListener('click', function() {
            // console.log(this.value);

            // remove all listeners when clicked
            for (let j = 0; j < choices.length; j++) {
               choices[j].style.pointerEvents = 'none';
            }

            // remove cut form
            cutForm.style.display = 'none';

            // change heading
            info.innerHTML = 'Your Turn: Double Click to Play a Card';

            // send clicked value to server to start game
            socket.emit('startRound', [this.value, player]);
         });
      }
   }

   else {
      info.innerHTML = 'Waiting on ' + player['username'];
   }
});

socket.on('showCut', function(cut) {
   let suits = ['spades', 'hearts', 'clubs', 'diamonds'];
   let t = suits[cut];

   let d = document.createElement('div');
   d.innerText = 'cut is ' + t;
   d.style.color = 'red';
   d.style.fontWeight = 'bold';
   d.style.padding = '2em';

   document.getElementById('header').appendChild(d);
});

socket.on('showTeams', function() {
   document.getElementById('teams').style.display = 'flex';

   // change team color 
   if (finalTeam == 0) {
      document.getElementById('tone').style.color = 'blue';
   }
   else if (finalTeam == 1) {
      document.getElementById('ttwo').style.color = 'blue';
   }
});

socket.on('chooseCard', function(endBoolean) {
   if (endBoolean) {
      socket.emit('findWinner');
   }
   
   // add double click event to every card  
   let d = hand[0];  // deck
   let ind = hand[1]; // card index

   // find index for displaying card
   for (let i = 0; i < players.length; i++) {
      let p = players[i];
      if (p['username'] == finalName) {
         position = i;
      }
   }

   // count is used to check if player has no valid cards
   let count = 0;
   for (let i = 0; i < ind.length; i++) {
      let c = d.cards[ind[i]];

      // if not first player and card is not the same suit as suit played
      // then increment count
      if (notFirst && c['suit'] != suitRound) {
         count += 1;
      }
   }


   for (let i = 0; i < ind.length; i++) {


      // add event listener to each card
      let c = d.cards[ind[i]];

      // console.log(notFirst, c['suit'], suitRound);

      if (count != ind.length) {
         if (notFirst && c['suit'] != suitRound) {
            continue;
         }
      }

      c['$el'].addEventListener('dblclick', function() {
         c.animateTo({
            delay: 0,
            duration: 200,
            ease: 'linear',
            x: 0 + (position * 100),
            y: 0
         });

         // remove eventListeners
         for (let j = 0; j < ind.length; j++) {
            let card = d.cards[ind[j]];
            card['$el'].style.pointerEvents = 'none';
         }

         // add label to card
         let suitNames = ['spades', 'hearts', 'clubs', 'diamonds'];
         let rank = c['rank'];
         var val = rank;
         var suit = suitNames[c['suit']];

         if (rank == 1) 
            val = 'ace';
         else if (rank == 11)
            val = 'jack';
         else if (rank == 12)
            val = 'queen';
         else if (rank == 13)
            val = 'king';

         // remove index from list
         let index = 0;
         for (let j = 0; j < ind.length; j++) {
            let card = d.cards[j];

            if (card['suit'] == c['suit'] && card['rank'] == c['rank']) {
               index = j;
            }
         }
         ind.splice(index, 1);


         socket.emit('nextPlayer', [val, suit, c, finalName, position])
      });
      
   }
});

// data is dictionary with keys: val, suit, player, team and nextPlayer
// val and suit are for the card that was played
// player is username of last player
// nextPlayer is player object of player that needs to play
// lastCard is the card object played by the last player
socket.on('updatePlayer', function(data) {
   // unpack data
   let val = data['val'];
   let suit = data['suit'];
   let prevPlayer = data['player']; // username of player of just played
   let team = data['team'];
   let nextPlayer = data['nextPlayer'];
   let lastCard = data['lastCard'];
   let prevPos = data['prevPos'];
   let endRound = data['endRound'];
   let whoPlayed = document.createElement('div');

   // select color
   whoPlayed.style.color = colors[team];
   whoPlayed.style.paddingBottom = '1em';

   // update client with who played
   if (prevPlayer == finalName) {
      whoPlayed.innerText = 'You:' + val + ' of ' + suit;
      // document.getElementById('header').appendChild(whoPlayed);
   }
   else {
      whoPlayed.innerText = prevPlayer + ': ' + val + ' of ' + suit;
      // document.getElementById('header').appendChild(whoPlayed);
   }

   // add whoPlayed to page
   if (team == 1) {
      document.getElementById('ttwo').appendChild(whoPlayed);
   }
   else {
      document.getElementById('tone').appendChild(whoPlayed);
   }

   // add lastCard to screen -> search through deck
   if (prevPlayer != finalName) {
      let deck = hand[0];
      for (let i = 0; i < deck.cards.length; i++) {
         let c = deck.cards[i];

         if (lastCard['rank'] == c['rank'] && lastCard['suit'] == c['suit']) {
            c.setSide('front');
            c['$el'].removeAttribute('style');

            c.animateTo({
               delay: 0,
               duration: 200,
               ease: 'linear',
               x: 0 + (prevPos * 100),
               y: 0
            });

            c.mount(document.getElementById('container'));
         }
      }
   }

   // only update header if all players have not played
   if (endRound) {
      // update info header to indicate who's turn
      if (nextPlayer['username'] == finalName) {
         document.getElementById('infoUpdate').innerHTML = 'Your Turn: Double Click to Play a Card';
      }
      else {
         document.getElementById('infoUpdate').innerHTML = 'Waiting for ' + nextPlayer['username'];
      }
   }

   // remove header
   else {  
      document.getElementById('infoUpdate').innerHTML = '';
   }

});

// suit is text of suit that was played
socket.on('updateSuit', function(suit) {
   let suits = ['spades', 'hearts', 'clubs', 'diamonds'];
   let d = document.createElement('div');
   d.innerText = suit + ' was played';
   document.getElementById('header').appendChild(d);
   notFirst = true;
   suitRound = suits.indexOf(suit);
});


// function for dealing animations
function fancyAnimations() {
   // create deck object
   var deck = Deck();

   var num_shuffles = 1;
   
   // coordinates for dealing
   var w = window.innerWidth;
   var h = window.innerHeight;
   var coordinates = [ [w, 0],
                  [w, -h],
                  [-w, -h],
                  [-w, 0],
                  [-w, h],
                  [w, h] ]

   // adds deck to DOM
   var main = document.getElementById('container');
   deck.mount(main);

   // shuffle animation
   // only 1 works using more causes delay
   
   for (let i = 0; i < num_shuffles; i++) {
      deck.shuffle();
   }

   // remove 2's from deck
   for (let i = 0; i < deck.cards.length; i++) {
      if (deck.cards[i]['rank'] == 2) {
         var two = deck.cards.splice(i, 1);
         two[0].unmount();
      }
   }

   // dealing animation
   for (let i = 0, j = 0; i < deck.cards.length; i++) {

      var location = coordinates[j];
      var card = deck.cards[i];

      card.animateTo({
         delay: 500 + i * 100,
         duration: 200,
         ease: 'linear',
         x: location[0],
         y: location[1]
      });

      // counter for coordinate index
      if (i % 8 == 0 && i != 0) {
         j += 1;
      }
   }

   // remove deck from page after animation
   setTimeout(function() {deck.unmount();}, 5500);
}

function showHand(players) {
   // get player of client
   var p;

   for (let i = 0; i < players.length; i++) {

      if (players[i]['username'] == finalName) {
         p = players[i];

         // update teamChoice for callUpdate event
         teamChoice = p['team'];
      }
   }

   // mount deck to DOM
   var deck = Deck();

   // get matching indices of player hands to deck
   var indices = [];
   for (let i = 0; i < p['hand'].length; i++) {
      var c = p['hand'][i];
      
      // get indices of player cards
      for (let j = 0; j < deck.cards.length; j++) {
         if (c.suit == deck.cards[j]['suit'] && c.value == deck.cards[j]['rank']) {
            indices.push(j);
         }   
      }
   }
   indices.sort();

   // remove cards from deck
   setTimeout(function() {
      deck.mount(document.getElementById('container'));
      for (let i = 0; i < deck.cards.length; i++) {
         if (!indices.includes(i)) {
            deck.cards[i].unmount();
         }
      }

       // show hand
      for (let i = 0; i < indices.length; i++) {
         var card = deck.cards[indices[i]];
         var w = window.innerWidth;
         var interval = w / 8;

         card.setSide('front');
         card['$el'].removeAttribute('style');

         card.animateTo({
            delay: 500 + i * 100,
            duration: 200,
            ease: 'linear',
            x: -w/2.35 + (interval * i),
            y: window.innerHeight / 2 * 0.8
         });
      }

   }, 6000);

   return [deck, indices];
}  // end function

  
