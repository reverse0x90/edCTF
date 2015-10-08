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
          id: 1,
          teamname: 'team1',
          title: 'Solve it',
          points: 500,
          correct_flags: 2,
          wrong_flags: 0,
          solved: [ 'Reversing 100', 'Web 400'],
        },
        {
          id: 2,
          teamname: 'team2',
          title: 'Solve it',
          points: 1337,
          correct_flags: 13,
          wrong_flags: 9322,
          solved: [ 'Reversing 783', 'Web 554'],
        },
      ]
    });
  });

  // GET teams/:id
  apiRouter.get('/teams/:id', function(req, res) {
    res.send({
     'teams': [ 
        {
          id: req.params.id,
          teamname: 'team1',
          title: 'Solve it',
          points: 500,
          correct_flags: 2,
          wrong_flags: 0,
          solved: [ 'Reversing 100', 'Web 400'],
        },
      ]
    });
  });
  
  app.use('/api/', apiRouter);
};
