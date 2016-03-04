import Ember from 'ember';

export default Ember.Controller.extend({
  settings: {},
  appController: null,
  scoreboardController: null,
  showHidden: false,
  sortTeams: ['points:desc', 'lasttimestamp:asc', 'id:asc'],
  sortedTeams: Ember.computed.sort('selectedScoreboard.teams', 'sortTeams'),
  rankedTeams: null,
  ctfSorting: ['online:desc', 'id'],
  sortedCtfs: Ember.computed.sort('model', 'ctfSorting'),
  selectedCtf: null,
  setSelectedCtf: function(){
    this.set('selectedCtf', this.get('appController').get('ctf'));
  }.observes('appController.ctf'),
  selectedScoreboard: null,
  setSelectedScoreboard: function(){
    this.set('selectedScoreboard', this.get('selectedCtf').get('scoreboard'));
  }.observes('selectedCtf'),
  setTeamRanks: function(){
    var teams = Ember.copy(this.get('sortedTeams'));
    var showHidden = this.get('showHidden');
    var position = 1;
    var i = 0;
    while(i < teams.length){
      if(teams[i].get('hidden')){
        if(showHidden){
          teams[i++].set('position', position++);
        } else {
          teams.removeAt(i);
        }
      } else {
        teams[i++].set('position', position++);
      }
    }
    this.set('rankedTeams', teams);
  }.observes('sortedTeams', 'showHidden').on('init'),
  actions:{
    promptConfirmation: function(messageArray, callback){
      this.set('modal.confirmMesg', messageArray);
      this.set('modal.confirmCallback', callback);
      this.set('modal.isConfirm', true);
    },
    changeSelectedCtf: function(ctf){
      this.set('selectedCtf', ctf);
    },
    closeTeam: function(){
      this.set('modal.isAdminTeam', false);
      this.set('modal.adminCtf', null);
      this.set('modal.adminScoreboard', null);
      this.set('modal.adminTeam', null);
      this.set('modal.errorMessage', '');
      this.set('modal.errorFields', {});
    },
    createTeam: function(newTeam){
      if(!newTeam.scoreboard){
        this.set('modal.errorFields', {});
        this.set('modal.errorMessage', 'Invalid scoreboard selected');
        return;
      }

      if(!newTeam.teamname){
        this.set('modal.errorFields', {'teamname': true});
        this.set('modal.errorMessage', 'Invalid team name');
        return;
      }

      if(!newTeam.username){
        this.set('modal.errorFields', {'username': true});
        this.set('modal.errorMessage', 'Invalid username');
        return;
      }

      if(!newTeam.email){
        this.set('modal.errorFields', {'email': true});
        this.set('modal.errorMessage', 'Invalid email');
        return;
      }

      if(!((newTeam.password).localeCompare(newTeam.confirmPassword))){
        this.set('modal.errorFields', {'password': true});
        this.set('modal.errorMessage', 'Passwords not equal');
        return;
      }


      var t = this;
      var team = t.store.createRecord('team', {
        scoreboard: newTeam.scoreboard,
        teamname: newTeam.teamname,
        username: newTeam.username,
        email: newTeam.email,
        password: newTeam.password,
      });
      team.save().then(function(){
        t.send('closeTeam');
      }, function(err){
        team.rollbackAttributes();
        if (err.errors.message){
          t.set('modal.errorMessage', err.errors.message);
        } else {
          t.set('modal.errorMessage', 'Server error, unable to add team');
        }
      });
    },
    openEditTeam: function(team){
      this.set('modal.adminCtf', this.get('selectedCtf'));
      this.set('modal.adminScoreboard', this.get('selectedScoreboard'));
      this.set('modal.adminTeam', team);
      this.set('modal.isAdminTeam', true);
    },
    editTeam: function(team, password, confirmPassword){
      if(!team.get('teamname')){
        this.set('modal.errorFields', {'teamname': true});
        this.set('modal.errorMessage', 'Invalid team name');
        return;
      }

      if(!team.get('username')){
        this.set('modal.errorFields', {'username': true});
        this.set('modal.errorMessage', 'Invalid username');
        return;
      }

      if(!team.get('email')){
        this.set('modal.errorFields', {'email': true});
        this.set('modal.errorMessage', 'Invalid email');
        return;
      }

      if(password){
        if(((password).localeCompare(confirmPassword))){
          this.set('modal.errorFields', {'password': true});
          this.set('modal.errorMessage', 'Passwords not equal');
          return;
        }
      } else {
        password = '';
      }

      var t = this;
      team.set('password', password);
      team.save().then(function(){
        t.send('closeTeam');
        team.set('password', undefined);
      }, function(err){
        team.rollbackAttributes();
        if (err.errors.message){
          t.set('modal.errorMessage', err.errors.message);
        } else {
          t.set('modal.errorMessage', 'Server error, unable to edit team');
        }
      });
    },
    deleteTeam: function(team){
      var t = this;
      this.send('promptConfirmation', [
        'This will delete user "' + team.get('username') + '".',
        'Are you sure?',
      ], function(confirmed){
        if(confirmed){
          team.deleteRecord();
          team.save().then(function(){
            t.send('closeTeam');
          }, function(err){
            team.rollbackAttributes();
            if (err.errors.message){
              t.set('modal.errorMessage', err.errors.message);
            } else {
              t.set('modal.errorMessage', 'Server error, unable to delete team');
            }
          });
        } else {
          t.set('modal.errorMessage', '');
          t.set('modal.errorFields', {});
        }
      });
    },
  },
});
