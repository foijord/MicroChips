
Deck : NSObject
{
  suits (class instance variable)
  ranks (class instance variable)

  + initialize
  {
    suits := {'c', 'd', 'h', 's'}.
    ranks := {'2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A'}.
  }

  + suits { ^ suits }
  + ranks { ^ ranks }

  + idFromCards: cards
  {
    | sorted |
    sorted := cards at: (ranks !@ cards) sort.
    ^ sorted \#++
  }
}.

Node : NSObject 
{
  nodeid

  - initWithCards: cards
  {
    self := super init.
    (self isEqual: nil) ifFalse:
    [
      nodeid := Deck idFromCards: cards
    ].
    ^ self
  }

  - nodeid { ^ nodeid }
}.

Deck initialize.

root := Node alloc initWithCards: { 'J', 'A', '7', '2' }.
root nodeid.
