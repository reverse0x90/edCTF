module.exports = function(app) {
  var express = require('express');
  var bodyParser = require('body-parser');
  var apiRouter = express.Router();
  
  apiRouter.use( bodyParser.json() );       // to support JSON-encoded bodies
  apiRouter.use( bodyParser.urlencoded({     // to support URL-encoded bodies
      extended: true
  }));

 apiRouter.get('/ctfs/:id', function(req, res) {
    res.send({
      'ctfs': [ 
        {
          id: 1,
          name: 'edCTF',
          challengeboard: [1],
          scoreboard: [1],
        },
      ],
    });
  });

  apiRouter.get('/challengeboards/:id', function(req, res) {
    res.send({
      'challengeboards': [ 
        {
          id: 1,
          categories: [1,2],
        },
      ],
      'categories': [ 
        {
          id: 1,
          name: 'Reversing',
          challenges: [1],
        },
        {
          id: 2,
          name: 'Exploit',
          challenges: [2,3,4],
        },
      ],
      'challenges': [ 
        {
          id: 1,
          title: 'Solve it',
          points: 100,
          description: 'Reverse it bro!',
          solved: false,
          num_solved: 0,
        },
        {
          id: 2,
          title: 'Solve it',
          points: 100,
          description: 'PWN it bro!',
          solved: false,
          num_solved: 0,
        },
        {
          id: 3,
          title: 'Solve it',
          points:200,
          description: 'PWN it bro!',
          solved: false,
          num_solved: 0,
        },
        {
          id: 4,
          title: 'Solve it',
          points: 300,
          description: 'PWN it bro!',
          solved: false,
          num_solved: 0,
        },
      ]
    });
  });

  apiRouter.get('/scoreboards/:id', function(req, res) {
    res.send({
      'scoreboards': [ 
        {
          id: 1,
          numtopteams: 10,
          teams: [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19]
        },
      ],
      'teams': [ 
        {
          id: 0,
          teamname: 'team0',
          points: 411,
          correct_flags: 12,
          wrong_flags: 16,
          solved: ['Reversing 783', 'Reversing 783'],
        },
        {
          id: 1,
          teamname: 'team1',
          points: 446,
          correct_flags: 19,
          wrong_flags: 38,
          solved: ['Reversing 783', 'Reversing 783'],
        },
        {
          id: 2,
          teamname: 'team2',
          points: 709,
          correct_flags: 8,
          wrong_flags: 30,
          solved: ['Reversing 783', 'Reversing 783', 'Reversing 783', 'Reversing 783'],
        },
        {
          id: 3,
          teamname: 'team3',
          points: 667,
          correct_flags: 9,
          wrong_flags: 29,
          solved: ['Reversing 783', 'Reversing 783', 'Reversing 783', 'Reversing 783', 'Reversing 783'],
        },
        {
          id: 4,
          teamname: 'team4',
          points: 418,
          correct_flags: 13,
          wrong_flags: 5,
          solved: ['Reversing 783', 'Reversing 783', 'Reversing 783'],
        },
        {
          id: 5,
          teamname: 'team5',
          points: 929,
          correct_flags: 7,
          wrong_flags: 45,
          solved: ['Reversing 783'],
        },
        {
          id: 6,
          teamname: 'team6',
          points: 671,
          correct_flags: 20,
          wrong_flags: 49,
          solved: ['Reversing 783', 'Reversing 783', 'Reversing 783', 'Reversing 783', 'Reversing 783'],
        },
        {
          id: 7,
          teamname: 'team7',
          points: 201,
          correct_flags: 14,
          wrong_flags: 31,
          solved: ['Reversing 783', 'Reversing 783', 'Reversing 783', 'Reversing 783', 'Reversing 783'],
        },
        {
          id: 8,
          teamname: 'team8',
          points: 196,
          correct_flags: 14,
          wrong_flags: 28,
          solved: ['Reversing 783', 'Reversing 783', 'Reversing 783', 'Reversing 783'],
        },
        {
          id: 9,
          teamname: 'team9',
          points: 83,
          correct_flags: 7,
          wrong_flags: 15,
          solved: ['Reversing 783'],
        },
        {
          id: 10,
          teamname: 'team10',
          points: 968,
          correct_flags: 19,
          wrong_flags: 29,
          solved: ['Reversing 783', 'Reversing 783', 'Reversing 783'],
        },
        {
          id: 11,
          teamname: 'team11',
          points: 186,
          correct_flags: 12,
          wrong_flags: 24,
          solved: ['Reversing 783', 'Reversing 783', 'Reversing 783', 'Reversing 783'],
        },
        {
          id: 12,
          teamname: 'team12',
          points: 93,
          correct_flags: 10,
          wrong_flags: 15,
          solved: ['Reversing 783'],
        },
        {
          id: 13,
          teamname: 'team13',
          points: 800,
          correct_flags: 14,
          wrong_flags: 4,
          solved: ['Reversing 783', 'Reversing 783', 'Reversing 783', 'Reversing 783'],
        },
        {
          id: 14,
          teamname: 'team14',
          points: 573,
          correct_flags: 13,
          wrong_flags: 28,
          solved: ['Reversing 783', 'Reversing 783', 'Reversing 783', 'Reversing 783', 'Reversing 783'],
        },
        {
          id: 15,
          teamname: 'team15',
          points: 740,
          correct_flags: 6,
          wrong_flags: 34,
          solved: ['Reversing 783'],
        },
        {
          id: 16,
          teamname: 'team16',
          points: 903,
          correct_flags: 11,
          wrong_flags: 43,
          solved: ['Reversing 783', 'Reversing 783', 'Reversing 783'],
        },
        {
          id: 17,
          teamname: 'team17',
          points: 379,
          correct_flags: 20,
          wrong_flags: 21,
          solved: ['Reversing 783', 'Reversing 783', 'Reversing 783', 'Reversing 783'],
        },
        {
          id: 18,
          teamname: 'team18',
          points: 595,
          correct_flags: 10,
          wrong_flags: 47,
          solved: ['Reversing 783'],
        },
        {
          id: 19,
          teamname: 'team19',
          points: 360,
          correct_flags: 7,
          wrong_flags: 38,
          solved: ['Reversing 783', 'Reversing 783', 'Reversing 783', 'Reversing 783'],
        },
      ]
    });
  });

  app.use('/api/', apiRouter);
};
