import Ember from 'ember';
import moment from 'moment';

export default Ember.Controller.extend({
  modal: {},
  ctf: null,
  authController: null,
  sortTeams: ['position'],
  sortedTeams: Ember.computed.sort('ctf.scoreboard.teams', 'sortTeams'),
  topTeamsData: {},
  setTopTeamsData: function(){
    if(!this.get('authController.isAuthenticated')){
      return;
    }

    var t = this;
    var currentTime = Date.now() / 1000 | 0;
    var tMinus = 60*5;

    var numTopTeams = this.get('ctf.scoreboard.numtopteams');
    var topTeamsData = {
      data: {
        xs: {},
        type: 'step',
        columns: [],
      },
     axis: {
        x: {
          tick: {
            fit: true,
            outer: false,
            count: 10,
            format: function (x) { 
                return moment(x*1000).utc().format('LLL');
            }
          },
          type: 'timeseries',
        },
        y: {
          min: 0,
          color: 'white',
          padding: {
            top:0,
            bottom:0
          },
          tick: {
            fit: true,
            outer: false,
          },
        },
      },
      point: {
        show: false
      },
      grid: {
        y: {
          show: true
        },
      },
      zoom: {
        enabled: true
      },
    };

    var challengeTimestampSort = function(a, b) { 
      if (a[1] > b[1]){
        return 1;
      }
      if (a[1] < b[1]){
        return -1;
      }
      return 0;
    };

    var teams = this.get('sortedTeams');
    this.get('ctf.challengeboard').then(function(){
      for(var i=0; i < numTopTeams && i < teams.length; i++){
        var points = 0;
        var timeData = [String(i)];
        var pointData = [teams[i].get('teamname')];
        
        var challengeTimestamps = teams[i].get('solves').sort(challengeTimestampSort);
        if(challengeTimestamps){
          for(var j=0; j < challengeTimestamps.length; j++){
            var id = challengeTimestamps[j][0];
            var timestamp = challengeTimestamps[j][1];
            var foundChallenge = t.store.peekRecord('challenge', id);

            if(j === 0){
              timeData.push(timestamp-tMinus);
              pointData.push(points);
            }

            if(foundChallenge){
              points = points + foundChallenge.get('points');
              timeData.push(timestamp);
              pointData.push(points);
            }
          }
          
          timeData.push(currentTime);
          pointData.push(teams[i].get('points'));
          topTeamsData.data.xs[teams[i].get('teamname')] = String(i);
          topTeamsData.data.columns.push(timeData);
          topTeamsData.data.columns.push(pointData);
        }
      }
      t.set('topTeamsData', topTeamsData);
    });
  }.observes('sortedTeams'),
  actions:{
    openTeamView: function(team){
      this.set('modal.team', team);
      this.set('modal.isTeam', true);
    }
  },
});
