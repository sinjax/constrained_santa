OK... so this might seem a bit overkill...
==========================================

The secret santa. A fun way of letting everyone get a gift, but making sure not everyone has to buy a gift for everyone else. This works well in small groups of poor friends and offices etc.

However, the small group of friends have a problem.

The group might involve a couple who are already getting each other presents. Or maybe there is a group of friends who are involved in another kind of gift giving. Furthermore how exactly do you assign santas? A hat with everyones name? What if you get your own name. Fine if you can throw it back in, but what if you want the constraints thing as well, you are given the hat and all the names are either your name or someone you can't have! 

You must start again.

Sounds like work to me, let's make the machines do our work!

So in this library there are two implementations of a constraint secret santa. 

One is old, badly written, but battle tested over 7 christmases (the self contained oldsanta.py).

Another constructs an acyclic graph and uses a breadth first algorithm in an attempt to find a looping path through the graph.

Enjoy!