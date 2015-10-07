module.exports = function(app) {
  var express = require('express');
  var bodyParser = require('body-parser');
  var apiRouter = express.Router();
  
  apiRouter.use( bodyParser.json() );       // to support JSON-encoded bodies
  apiRouter.use( bodyParser.urlencoded({     // to support URL-encoded bodies
      extended: true
  }));
  
  // POST login
  apiRouter.post('/login', function(req, res) {
    var status = false;
    if (req.body.username && req.body.password){
      status = true;
    }
    
    res.send({
      success: status,
      username: req.body.username,
    });
  });

  // POST register
  apiRouter.post('/register', function(req, res) {
    var status = false;
    if (req.body.username && req.body.password && req.body.teamname){
      status = true;
    }
    
    res.send({
      success: status,
      username: req.body.username,
      teamname: req.body.teamname,
    });
  });
  
  // GET challenges
  apiRouter.get('/challenges', function(req, res) {
    res.send([
      {
        id: 1,
        category: 'Reversing',
        title: 'Solve it',
        points: 100,
        description: 'solve it bro', 
        solved: false,
        num_solved: 0,
        links: {
          'binary': '/path/to/rev100',
        },
      },
    ]);
  });

  // GET challenges/:id
  apiRouter.get('/challenges/:id', function(req, res) {
    res.send({
      id: req.params.id,
      category: 'Reversing',
      title: 'Solve it',
      points: 100,
      description: 'solve it bro',
      solved: false,
      num_solved: 0,
      links: {
        'binary': '/path/to/rev100',
      },
    });
  });


  // POST challenges/:id
  apiRouter.post('/challenges/:id', function(req, res) {
    var status = false;
    if (req.body.flag && !isNaN(req.params.id)){
      if (req.params.id % 2 == 0){
        status = true;
      }
    }
    
    res.send({
      success: status,
      points: 200, // points awarded
    });
  });

  // GET teams
  apiRouter.get('/teams', function(req, res) {
    res.send([
      {
        id: 1,
        teamname: 'team1',
        points: 500,
        correct_flags: 0,
        wrong_flags: 0,
        solved: [
          'Reversing 100',
          'Web 400',
        ],
      },
    ]);
  });

  // GET teams/:id
  apiRouter.get('/teams/:id', function(req, res) {
    res.send({
      id: req.params.id,
      teamname: 'team1',
      points: 500,
      correct_flags: 0,
      wrong_flags: 0,
      solved: [
        'Reversing 100',
        'Web 400',
      ]
    });
  });
  
  // POST teams/:id
  apiRouter.post('/teams/:id', function(req, res) {
    if (req.body.password){ // ADD MORE (?)
      var password = req.body.password;
      res.send({
        success: true,
        message: "something something, send confirmation email..."
      });
    }
    else {
      res.send({
        success: true,
      });
    }
  });

  app.use('/api/', apiRouter);
};
