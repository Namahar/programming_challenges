const express = require('express');
const socketio = require('socket.io');

const app = express()
const port = 5000;
const server = app.listen(port);
const io = socketio(server)

var players = [];
var num_players = 6;
var calls = [];
var dealer = 0;
var round = 0;
var cardsPlayed = [];
var cut;

// suit of first card played in round
var firstPlayed;

// used to keep track of how many people called
var count = 0;

// used to determine if players are ready to call
var callReady = 0;
var firstPlayer = 0;

class Card {
   constructor(suit, value) {
      this.suit = suit;
      this.value = value;
   }
}

function printDeck(deck) {
   console.log(deck.length);

   // card is an index value
   for (var card in deck) {

      // get object and print values
      var c = deck[card];
      console.log(c.suit, c.value);
   }
}

function createDeck() {
   
   // gaunt doesn't use 2's
   var suits = 4;

   // create deck
   var deck = [];

   // used for shuffling
   var i = 0, j = 0, temp = null;
   
   // loop through card values
   for (i = 1; i <= 13; i++) {

      // skips 2's
      if (i == 2) {
         continue;
      } 
      
      // loop through suit values
      for (j = 0; j < suits; j++) {
         c = new Card(j, i);
         deck.push(c);
      }
   }

   // shuffle deck
   for (i = deck.length - 1; i >= 0; i -= 1) {
      j = Math.floor(Math.random() * (i + 1));
      temp = deck[i];
      deck[i] = deck[j];
      deck[j] = temp;
   }

   return deck;
}

function swap(cards, i, j) {
   var temp = cards[j];
   cards[j] = cards[i];
   cards[i] = temp;

   return;
}

function sortCards(cards) {
   // order is spades, hearts, clubs diamonds
   // cards have suit and value
   // implement bubble sort for suits
   for (let i = 0 ; i < cards.length - 1; i++) {
      
      for (let j = 0; j < cards.length - i - 1; j++) {

         if (cards[j].suit > cards[j + 1].suit) {
            swap(cards, j, j+1);
         }

         // suits are same order by value
         if (cards[j].suit == cards[j+1].suit) {

            if (cards[j].value > cards[j+1].value) {
               swap(cards, j, j+1);
            }
         }

      }  // end for loop of index j
   }  // end for loop of index i
}  // end function

function checkValue(data) {
   var count = 0;

   // check how many times a value is chosen
   for (let i = 0; i < players.length; i++) {
      p = players[i];
      if (p['team'] == data) {
         count += 1;
      }

      // console.log(p['team'], data, count);
   }
   // console.log();

   // if value is chosen more than 3 times
   // team is full
   if (count > 2)
      return false;
   else
      return true;
}

console.log('server is running');

app.get('/', function (request, response) {
   response.send('<h1>Gaunt Server</h1>');
});

io.on('connection', function(socket) {
   io.emit('teamUpdate', players);

   socket.on('waiting', function(data) {
      if (players.length < num_players) {

         // check if socket is already in stack
         if (!players.includes(socket)) {
            var teamValue = checkValue(data['teamChoice']);

            var player = {
               'socket': socket.id,
               'username': data['socketName']
            };

            if (teamValue) {
               player['team'] = data['teamChoice'];
            }
            else {
               player['team'] = data['teamChoice'] ^ 1;
            }
            
            players.push(player);
            io.emit('teamUpdate', players);
         }

         // 6 players have joined game
         if (players.length == num_players) {

            // reorder players array
            for (let i = 0; i < players.length - 1; i++) {
               let p = players[i];
               let q = players[i+1];

               // same team need to alternate
               if (p['team'] == q['team']) {
                  for (let j = i+1; j < players.length; j++) {
                     let t = players[j];

                     if (t['team'] != q['team']) {
                        let temp = players[i+1];
                        players[i+1] = players[j];
                        players[j] = temp;
                     }
                  } 
               }
            }

            for (let i = 0; i < players.length; i++) {
               let p = players[i];
               console.log(p['team']);
            }

            // add cards to players hand
            var serverDeck = createDeck();
            // printDeck(serverDeck);

            for (let i = 0; i < players.length; i++) {
               // get player
               var p = players[i];
               p['hand'] = [];

               for (let j = 0; j < 8; j++) {
                  var serverCard = serverDeck.pop();
                  p['hand'].push(serverCard);
               }

               // sort cards - spades, hearts, clubs diamonds
               sortCards(p['hand']);
            }

            // send data to client
            io.emit('start', players);
            
            // prints teams
            console.log('game full');
            for (let i = 0; i < players.length; i++) {
               p = players[i];
               console.log(p['username'], p['socket'], p['team'], p['hand']);
            }
            console.log();
         }
      }
   });

   // starts calling process
   socket.on('startCall', function(value) {
      callReady += value;

      // check when to stop initial calling
      if (count == 6) {
         io.emit('raiseCalls');
      }

      else if (callReady == 6) {
         
         // send response to first socket indicated by 1
         // lets user know to call
         p = players[dealer];
         socket.broadcast.to(p['socket']).emit('signalCall', [1, p['username']]);

         // loop through players
         // other players are notified of who is calling
         for (let i = 0; i < num_players; i++) {
            
            if (i != dealer) {
               var temp = players[i];

               io.to(temp['socket']).emit('signalCall', [0, p['username']]);
            }
         }        
      }

   });

   // connection to get calls from individual players
   // data is dictionary with keys 'username' and 'numCalls'
   socket.on('call', function(data) {
      count += 1;

      if (count < 12) {
         let p;

         // seach player and add call value
         for (let i = 0; i < players.length; i++) {
            var player = players[i];

            if (data['username'] == player['username']) {
               player['handsCalled'] = data['numCalls'];
               p = player;
            }
         }

         calls.push(data);
         console.log(data);

         // io.emit('updateCall', players);
         io.emit('updateCall', p);

         // pick player on other team; next person calls
         dealer += 1;

         // check if dealer is out of bounds
         if (dealer >= 6) {
            dealer = 0;
         }
      }

      // raising is done pick player with highest call
      else if (count == 12) {
         console.log(count);
         io.emit('finishCall');

         // pick player to start
         var index;
         var maxHands = -1;
         for (let i = 0; i < players.length; i++) {
            let p = players[i];

            if (p['handsCalled'] > maxHands) {
               index = i;
               maxHands = p['handsCalled'];
            }
         }

         // check if maxHands is 0
         // if all calls are 0, last player is chosen
         if (maxHands == 0) {
            index = num_players - 1;
         }

         // ask player for cut
         io.emit('cut', players[index]);

         console.log(index, players[index]['username']);
      }

   });

   socket.on('raiseCall', function() {
   
      p = players[dealer];

      socket.broadcast.to(p['socket']).emit('signalCall', [2, p['username']]);

      // loop through players
      // other players are notified of who is calling
      for (let i = 0; i < num_players; i++) {
         
         if (i != dealer) {
            var temp = players[i];

            io.to(temp['socket']).emit('signalCall', [0, p['username']]);
         }
      }
      
   });

   socket.on('startRound', function(data) {
      // unpack data
      cut = data[0];
      let p = data[1];

      // show cut to all players
      io.emit('showCut', cut);

      console.log(p);

      // increase round counter
      round += 1;

      // indicate that suit needs to be stored from next player
      firstPlayer = 1;  

      // show all clients the teams
      io.emit('showTeams');
      
      // let player select a card
      io.to(p['socket']).emit('chooseCard');
   });

   // next player 
   // input data is array of val, suit, card, and username of last player
   // card has rank and suit attributes
   socket.on('nextPlayer', function(data) {
      console.log();

      // emit update to what was played to all players
      let val = data[0];
      let rank = data[1];
      let card = data[2];
      let prevPlayer = data[3]; 
      let position = data[4];
      let t;

      // add card to array
      let cardData = {};
      cardData['username'] = prevPlayer;
      cardData['value'] = card['rank'];
      cardData['suit'] = card['suit'];
      cardsPlayed.push(cardData);
      
      // remove card from previous player hand
      for (let i = 0; i < num_players; i++) {
         let p = players[i];

         if (p['username'] == prevPlayer) {
            // store team info for client colors
            t = p['team'];

            // find card just played and remove
            for (let j = 0; j < p['hand'].length; j++) {
               let playerCard = p['hand'][j];

               // splice card from hand
               if (playerCard['suit'] == card['suit'] && playerCard['value'] == card['rank']) {
   
                  // remove card
                  p['hand'].splice(j, 1);
                  console.log(p['hand']);
               }
            }
         }
      }

      // check if all players have played
      // hand will match round count
      var allPlayed = 0;
      for (let i = 0; i < num_players; i++) {
         let p = players[i];

         if (p['hand'].length == 8 - round) {
            allPlayed += 1;
         }
      }

      console.log('allplayed = ' + allPlayed);

      // not everyone has played send input to next player
      // don't need to check for out of bounds
      // if i = 5 -> last player will play 
      if (allPlayed <= num_players) {
         var nextPlayer = -1;

         // search for next player
         for (let i = 0; i < num_players - 1; i++) {
             let p = players[i];
             if (p['username'] == prevPlayer) {
               nextPlayer = i + 1;
             }
         }

         if (nextPlayer == -1) {
            nextPlayer = 0;
         }

         // send socket to next player
         let p = players[nextPlayer];
         console.log();
         console.log(p);         

         endRound = true;
         if (allPlayed == num_players) {
            endRound = false;
         }

         // update info for other players
         let data = {'val': val,
                     'suit': rank,
                     'player': prevPlayer,
                     'team': t,
                     'nextPlayer': p,
                     'lastCard': card,
                     'prevPos': position,
                     'endRound': endRound
                     }
         
         // alert clients to what suit was played and reset variable
         if (firstPlayer == 1) {
            firstPlayed = c['suit'];
            io.emit('updateSuit', rank);
            firstPlayer = 0;
         }

         // update info of who played
         io.emit('updatePlayer', data);

         if (allPlayed == num_players) {
            io.to(p['socket']).emit('chooseCard', true);
         }
         else {
            io.to(p['socket']).emit('chooseCard', false);
         }
      }
      
      

   //    // all players have played
   //    // round is over
   //    if (allPlayed == num_players) {
   //       console.log();
   //       console.log('cut = ' + cut);

   //       let numCut = 0;
   //       let oneCut = 0;
   //       let winningPlayer;
   //       let winningCard = 0;

   //       // search cards for number of cut
   //       for (let i = 0; i < num_players; i++) {
   //          let c = cardsPlayed[i];
   //          if (c['suit'] == cut) {
   //             numCut += 1;

   //             // if numCut is one keep track of index
   //             // in case only one cut is played 
   //             if (numCut == 1) {
   //                oneCut = i;
   //             }
   //          }
   //       }

   //       console.log('numCut = ' + numCut);

   //       // someone cut and won
   //       if (numCut == 1) {
   //          winningCard = cardsPlayed[oneCut]['value'];
   //          winningPlayer = cardsPlayed[oneCut]['username'];
   //       }

   //       // multiple people cut -> find winner
   //       else if (numCut > 1) {
   //          for (let i = 0; i < num_players; i++) {
   //             let c = cardsPlayed[i];

   //             if (c['suit'] == cut) {
   //                if (c['value'] == 1) {
   //                   winningCard = 1;
   //                   winningPlayer = c['username'];
   //                   break;
   //                }

   //                if (c['value'] > winningCard) {
   //                   winningCard = c['value'];
   //                   winningPlayer = c['username'];
   //                }
   //             }
   //          }
   //       }

   //       // cut was not played -> find highest card of matching suit
   //       else if (numCut == 0) {
   //          for (let i = 0; i < num_players; i++) {
   //             let c = cardsPlayed[i];

   //             if (c['suit'] == firstPlayed) {
   //                if (c['value'] == 1) {
   //                   winningCard = 1;
   //                   winningPlayer = c['username'];
   //                   break;
   //                }
                  
   //                if (c['rank'] > winningCard) {
   //                   winningCard = c['rank'];
   //                   winningPlayer = c['username'];
   //                }
   //             } 
   //          }
   //       }

   //       console.log(winningPlayer, winningCard);

   //       // remove cards from client
   //       console.log(cardsPlayed);
   //    }
   });

   socket.on('nextPlayer', function(data) {
      console.log();
   });

});
