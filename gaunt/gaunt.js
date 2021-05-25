// suit values range from 1 - 4
// card values range from 3 - 14
// jack = 11, queen = 12, king = 13, ace = 14

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

function setup() {
   
   // gaunt doesn't use 2's
   var deck_len = 48;
   var suits = 4;

   // create deck
   var deck = [];

   // used for shuffling
   var i = 0, j = 0, temp = null;
   
   // loop through card values
   for ( i = 3; i <= (deck_len / suits) + 2; i++) {
      
      // loop through suit values
      for (j = 1; j <= suits; j++) {
         c = new Card(j, i);
         deck.push(c);
      }
   }

   // shuffle deck
   for (var i = deck.length - 1; i >= 0; i -= 1) {
      j = Math.floor(Math.random() * (i + 1));
      temp = deck[i];
      deck[i] = deck[j];
      deck[j] = temp;
   }

   return deck;
}


deck = setup();
printDeck(deck);

