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
              live: true,
              challengeboard: [1],
              scoreboard: [1],
            },
          ],
        });
  });

  apiRouter.get('/ctfs', function(req, res) {
    var ctfs = [ 
      {
        id: 1,
        name: 'edCTF',
        live: true,
        challengeboard: [1],
        scoreboard: [1],
      },
      {
        id: 2,
        name: 'edCTF2',
        live: false,
        challengeboard: [1],
        scoreboard: [1],
      },
      {
        id: 3,
        name: 'edCTF3',
        live: false,
        challengeboard: [1],
        scoreboard: [1],
      },
    ];
    if (req.query.live == 'true'){
      var liveCTF = {};
      for (var i=0; i < ctfs.length; i++){
        if(ctfs[i].live){
          liveCTF = ctfs[i];
          break;
        }
      }
      res.send({
        'ctfs': [ 
          liveCTF
        ],
      });
    } else {
      res.send({
        'ctfs': ctfs,
      });
    }
  });


  apiRouter.get('/challengeboards/:id', function(req, res) {
    res.send({
      'challengeboards': [ 
        {
          id: 1,
          categories: [1,2,3,4,5,6,7],
        },
      ],
      'categories': [ 
        {
          id: 1,
          name: 'Trivia',
          challenges: [1,2,3,4,5],
        },
        {
          id: 2,
          name: 'Recon',
          challenges: [6,7,8,9],
        },
        {
          id: 3,
          name: 'Web',
          challenges: [10,11],
        },
        {
          id: 4,
          name: 'Reversing',
          challenges: [12,13,14,15],
        },
        {
          id: 5,
          name: 'Exploitation',
          challenges: [16,17,18,19,20],
        },
        {
          id: 6,
          name: 'Forensics',
          challenges: [21,22,23,24],
        },
        {
          id: 7,
          name: 'Networking',
          challenges: [25,26,27],
        },
      ],
      'challenges': [ 
        {
          id: 1,
          title: 'Solve it',
          points: 100,
          description: 'Trivia it bro!',
          solved: false,
          num_solved: 0,
        },
        {
          id: 2,
          title: 'Solve it',
          points: 200,
          description: 'Trivia it bro!',
          solved: false,
          num_solved: 0,
        },
        {
          id: 3,
          title: 'Solve it',
          points: 400,
          description: 'Trivia it bro!',
          solved: false,
          num_solved: 0,
        },
        {
          id: 4,
          title: 'Solve it',
          points: 400,
          description: 'Trivia it bro!',
          solved: true,
          num_solved: 0,
        },
        {
          id: 5,
          title: 'Solve it',
          points: 500,
          description: 'Trivia it bro!',
          solved: false,
          num_solved: 0,
        },
        {
          id: 6,
          title: 'Solve it',
          points: 100,
          description: 'Recon it bro!',
          solved: false,
          num_solved: 0,
        },
        {
          id: 7,
          title: 'Solve it',
          points: 200,
          description: 'Recon it bro!',
          solved: true,
          num_solved: 0,
        },
        {
          id: 8,
          title: 'Solve it',
          points: 400,
          description: 'Recon it bro!',
          solved: false,
          num_solved: 0,
        },
        {
          id: 9,
          title: 'Solve it',
          points: 500,
          description: 'Recon it bro!',
          solved: false,
          num_solved: 0,
        },
        {
          id: 10,
          title: 'Solve it',
          points: 400,
          description: 'Web it bro!',
          solved: false,
          num_solved: 0,
        },
        {
          id: 11,
          title: 'Solve it',
          points: 400,
          description: 'Web it bro!',
          solved: false,
          num_solved: 0,
        },
        {
          id: 12,
          title: 'Solve it',
          points: 100,
          description: 'Reverse it bro!',
          solved: false,
          num_solved: 0,
        },
        {
          id: 13,
          title: 'Solve it',
          points: 200,
          description: 'Reverse it bro!',
          solved: false,
          num_solved: 0,
        },
        {
          id: 14,
          title: 'Solve it',
          points: 400,
          description: 'Reverse it bro!',
          solved: false,
          num_solved: 0,
        },
        {
          id: 15,
          title: 'Solve it',
          points: 400,
          description: 'Reverse it bro!',
          solved: false,
          num_solved: 0,
        },
        {
          id: 16,
          title: 'Solve it',
          points: 100,
          description: 'Exploit it bro!',
          solved: true,
          num_solved: 0,
        },
        {
          id: 17,
          title: 'Solve it',
          points: 200,
          description: 'Exploit it bro!',
          solved: false,
          num_solved: 0,
        },
        {
          id: 18,
          title: 'Solve it',
          points: 400,
          description: 'Exploit it bro!',
          solved: false,
          num_solved: 0,
        },
        {
          id: 19,
          title: 'Solve it',
          points: 400,
          description: 'Exploit it bro!',
          solved: false,
          num_solved: 0,
        },
        {
          id: 20,
          title: 'Solve it',
          points: 500,
          description: 'Exploit it bro!',
          solved: false,
          num_solved: 0,
        },
        {
          id: 21,
          title: 'Solve it',
          points: 100,
          description: 'Forensic it bro!',
          solved: false,
          num_solved: 0,
        },
        {
          id: 22,
          title: 'Solve it',
          points: 400,
          description: 'Forensic it bro!',
          solved: false,
          num_solved: 0,
        },
        {
          id: 23,
          title: 'Solve it',
          points: 400,
          description: 'Forensic it bro!',
          solved: false,
          num_solved: 0,
        },
        {
          id: 24,
          title: 'Solve it',
          points: 500,
          description: 'Forensic it bro!',
          solved: false,
          num_solved: 0,
        },
        {
          id: 25,
          title: 'Solve it',
          points: 100,
          description: 'Network it bro!',
          solved: false,
          num_solved: 0,
        },
        {
          id: 26,
          title: 'Solve it',
          points: 200,
          description: 'Network it bro!',
          solved: false,
          num_solved: 0,
        },
        {
          id: 27,
          title: 'Solve it',
          points: 400,
          description: 'Network it bro!',
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
          topteamsdata: {
            x: 'x',
            //        xFormat: '%Y%m%d', // 'xFormat' can be used as custom format of 'x'
            columns: [
              ['x', '2013-01-01', '2013-01-02', '2013-01-03',],
              //            ['x', '20130101', '20130102', '20130103', '20130104', '20130105', '20130106'],
              //['data1', 30, 200, 100, 400, 150, 250],
              //['data2', 130, 340, 200, 500, 250, 350]
              ["team0", 0, 299, 1000],
              ["team1", 0, 732, 975],
              ["team2", 0, 929, 953],
              ["team3", 0, 670, 933],
              ["team4", 0, 362, 933],
              ["team5", 0, 490, 918],
              ["team6", 0, 722, 893],
              ["team7", 0, 632, 876],
              ["team8", 0, 274, 875],
              ["team9", 0, 768, 872],
            ],
          },
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
