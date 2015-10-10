module.exports = function(app) {
  var express = require('express');
  var bodyParser = require('body-parser');
  var apiRouter = express.Router();
  
  apiRouter.use( bodyParser.json() );       // to support JSON-encoded bodies
  apiRouter.use( bodyParser.urlencoded({     // to support URL-encoded bodies
      extended: true
  }));
  
  // GET challenges
 apiRouter.get('/challenges', function(req, res) {
    res.send({
      'challenges': [ 
        {
          id: 1,
          category: 'Reversing',
          title: 'Solve it',
          points: 100,
          description: 'Reverse it bro!',
          solved: false,
          num_solved: 0,
        },
        {
          id: 2,
          category: 'Exploit',
          title: 'Solve it',
          points: 100,
          description: 'PWN it bro!',
          solved: false,
          num_solved: 0,
        },
      ]
    });
  });

  // GET challenges/:id
  apiRouter.get('/challenges/:id', function(req, res) {
    res.send({
     'challenges': [ 
        {
          id: req.params.id,
          category: 'Reversing',
          title: 'Solve it',
          points: 100,
          description: 'Reverse it bro!',
          solved: false,
          num_solved: 0,
        },
      ]
    });
  });

  // GET teams
  apiRouter.get('/teams', function(req, res) {
    res.send({
     'teams': [ 
        {
          id: 0,
          teamname: 'team0',
          points: 198,
        },
        {
          id: 1,
          teamname: 'team1',
          points: 409,
        },
        {
          id: 2,
          teamname: 'team2',
          points: 40,
        },
        {
          id: 3,
          teamname: 'team3',
          points: 816,
        },
        {
          id: 4,
          teamname: 'team4',
          points: 716,
        },
        {
          id: 5,
          teamname: 'team5',
          points: 693,
        },
        {
          id: 6,
          teamname: 'team6',
          points: 684,
        },
        {
          id: 7,
          teamname: 'team7',
          points: 406,
        },
        {
          id: 8,
          teamname: 'team8',
          points: 302,
        },
        {
          id: 9,
          teamname: 'team9',
          points: 184,
        },
        {
          id: 10,
          teamname: 'team10',
          points: 438,
        },
        {
          id: 11,
          teamname: 'team11',
          points: 919,
        },
        {
          id: 12,
          teamname: 'team12',
          points: 286,
        },
        {
          id: 13,
          teamname: 'team13',
          points: 791,
        },
        {
          id: 14,
          teamname: 'team14',
          points: 914,
        },
        {
          id: 15,
          teamname: 'team15',
          points: 351,
        },
        {
          id: 16,
          teamname: 'team16',
          points: 769,
        },
        {
          id: 17,
          teamname: 'team17',
          points: 693,
        },
        {
          id: 18,
          teamname: 'team18',
          points: 105,
        },
        {
          id: 19,
          teamname: 'team19',
          points: 186,
        },
      ]
    });
  });

  // GET teams/:id
  apiRouter.get('/teams/:id', function(req, res) {
    res.send({
     'team': [ 
        {
          id: req.params.id,
          teamname: 'team'+req.params.id,
          points: 100,
          correct_flags: 10,
          wrong_flags: 51,
          solved: [ 'Reversing 100', 'Web 400'],
        },
      ]
    });
  });
  
  app.use('/api/', apiRouter);
};
