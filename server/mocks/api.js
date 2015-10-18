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
          name: 'Exploit',
          challenges: [2,3,4],
        },
        {
          id: 2,
          name: 'Reversing',
          challenges: [1],
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
          topteams: [
            [
              "",
              "team0",
              "team1",
              "team2",
              "team3",
              "team4",
              "team5",
              "team6",
              "team7",
              "team8",
              "team9",
            ],[
              "Time 1",
              0,
              0,
              0,
              0,
              0,
              0,
              0,
              0,
              0,
              0,
            ],[
              "Time 2",
              299,
              732,
              929,
              670,
              362,
              490,
              722,
              632,
              274,
              768,
            ],[
              "Time 3",
              1000,
              975,
              953,
              933,
              933,
              918,
              893,
              876,
              875,
              872,
            ]
          ],
          teams: [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19]
        },
      ],
      'teams': [ 
        {
          id: 0,
          teamname: 'team0',
          points: 1000,
          correct_flags: 7,
          wrong_flags: 10,
          solved: ['Reversing 783'],
        },
        {
          id: 1,
          teamname: 'team1',
          points: 975,
          correct_flags: 5,
          wrong_flags: 30,
          solved: ['Reversing 783', 'Reversing 783', 'Reversing 783', 'Reversing 783', 'Reversing 783'],
        },
        {
          id: 2,
          teamname: 'team2',
          points: 953,
          correct_flags: 15,
          wrong_flags: 34,
          solved: ['Reversing 783', 'Reversing 783', 'Reversing 783', 'Reversing 783'],
        },
        {
          id: 3,
          teamname: 'team3',
          points: 933,
          correct_flags: 3,
          wrong_flags: 2,
          solved: ['Reversing 783', 'Reversing 783'],
        },
        {
          id: 4,
          teamname: 'team4',
          points: 933,
          correct_flags: 15,
          wrong_flags: 3,
          solved: ['Reversing 783'],
        },
        {
          id: 5,
          teamname: 'team5',
          points: 918,
          correct_flags: 18,
          wrong_flags: 24,
          solved: ['Reversing 783', 'Reversing 783', 'Reversing 783', 'Reversing 783'],
        },
        {
          id: 6,
          teamname: 'team6',
          points: 893,
          correct_flags: 10,
          wrong_flags: 30,
          solved: ['Reversing 783', 'Reversing 783'],
        },
        {
          id: 7,
          teamname: 'team7',
          points: 876,
          correct_flags: 8,
          wrong_flags: 4,
          solved: ['Reversing 783', 'Reversing 783', 'Reversing 783', 'Reversing 783', 'Reversing 783'],
        },
        {
          id: 8,
          teamname: 'team8',
          points: 875,
          correct_flags: 18,
          wrong_flags: 35,
          solved: ['Reversing 783', 'Reversing 783'],
        },
        {
          id: 9,
          teamname: 'team9',
          points: 872,
          correct_flags: 5,
          wrong_flags: 28,
          solved: ['Reversing 783'],
        },
        {
          id: 10,
          teamname: 'team10',
          points: 868,
          correct_flags: 2,
          wrong_flags: 22,
          solved: ['Reversing 783', 'Reversing 783', 'Reversing 783', 'Reversing 783', 'Reversing 783'],
        },
        {
          id: 11,
          teamname: 'team11',
          points: 868,
          correct_flags: 2,
          wrong_flags: 4,
          solved: ['Reversing 783', 'Reversing 783', 'Reversing 783'],
        },
        {
          id: 12,
          teamname: 'team12',
          points: 848,
          correct_flags: 16,
          wrong_flags: 42,
          solved: ['Reversing 783', 'Reversing 783', 'Reversing 783'],
        },
        {
          id: 13,
          teamname: 'team13',
          points: 823,
          correct_flags: 15,
          wrong_flags: 20,
          solved: ['Reversing 783', 'Reversing 783'],
        },
        {
          id: 14,
          teamname: 'team14',
          points: 809,
          correct_flags: 20,
          wrong_flags: 33,
          solved: ['Reversing 783'],
        },
        {
          id: 15,
          teamname: 'team15',
          points: 804,
          correct_flags: 11,
          wrong_flags: 21,
          solved: ['Reversing 783'],
        },
        {
          id: 16,
          teamname: 'team16',
          points: 794,
          correct_flags: 10,
          wrong_flags: 14,
          solved: ['Reversing 783', 'Reversing 783', 'Reversing 783', 'Reversing 783', 'Reversing 783'],
        },
        {
          id: 17,
          teamname: 'team17',
          points: 771,
          correct_flags: 12,
          wrong_flags: 10,
          solved: ['Reversing 783', 'Reversing 783'],
        },
        {
          id: 18,
          teamname: 'team18',
          points: 756,
          correct_flags: 6,
          wrong_flags: 34,
          solved: ['Reversing 783', 'Reversing 783', 'Reversing 783'],
        },
        {
          id: 19,
          teamname: 'team19',
          points: 746,
          correct_flags: 5,
          wrong_flags: 28,
          solved: ['Reversing 783', 'Reversing 783', 'Reversing 783'],
        },
      ]
    });
  });

  app.use('/api/', apiRouter);
};
