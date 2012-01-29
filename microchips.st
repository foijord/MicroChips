
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
  nodecache (class instance variable)

  + initialize
  {
    nodecache := #{}
  }

  + getOrCreateNode: cards
  {
    | node id |
    id := Deck idFromCards: cards.
    node := nodecache valueForKey: id.

    (node ~~ nil) ifFalse:
    [
      node := Node alloc initWithId: id.
      nodecache setValue: node forKey: id.
    ].
    ^ node
  }

  - initWithId: id
  {
    self := super init.
    (self ~~ nil) ifTrue:
    [
      nodeid := id
    ].
    ^ self
  }

  - nodeid { ^ nodeid }
}.


node1 := Node getOrCreateNode: { 'J', 'A', '7', '2' }.
node2 := Node getOrCreateNode: { 'A', 'J', '2', '7' }.

node1 isEqual: node2.
