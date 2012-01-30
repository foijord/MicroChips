
ranks := {'2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A'}
id := [:a :b | { a, b } \ #++ ]
sort := [:c | c at: (ranks !@ c) sort]

level0 := ranks subpartsOfSize:1
level1 := (sort value: @((level0 @1 ++ @2 level0) \ #++)) distinct
level2 := (sort value: @((level1 @1 ++ @2 level1) \ #++)) distinct
level3 := (sort value: @((level2 @1 ++ @2 level2) \ #++)) distinct

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

    (node == nil) ifTrue:
    [
      node := Node alloc initWithId: id.
      nodecache setValue: node forKey: id.
    ].
    ^ node
  }

  - initWithId: id
  {
    self := super init.
    (self == nil) ifFalse:
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
