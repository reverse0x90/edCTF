import Ember from 'ember';
import moment from 'moment';

export default Ember.Controller.extend({
  modal: {},
  ctf: null,
  session: null,
  numTopTeams: 0,
  //sortTeams: ['position'],
  sortTeams: ['points:desc', 'lasttimestamp:asc', 'id:asc'],
  sortedTeams: Ember.computed.sort('ctf.scoreboard.teams', 'sortTeams'),
  setTeamRanks: function(){
    var teams = this.get('sortedTeams');
    for (var i=0; i < teams.length; i++){
      teams[i].set('position', i+1);
    }
  }.observes('sortedTeams'),
  topTeamsData: {},
  setTopTeamsData: function(){
    if(!this.get('session.isAuthenticated')){
      return;
    } else {
      if(!this.get('ctf')){
        return;
      }
    }

    var t = this;
    var currentTime = Date.now() / 1000 | 0;
    var tMinus = 60*5;

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
    var numTopTeams = this.get('ctf.scoreboard.numtopteams');
    if(teams.length < numTopTeams ){
      numTopTeams = teams.length;
    }

    this.get('ctf.challengeboard').then(function(){
      for(var i=0; i < numTopTeams; i++){
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
      t.set('numTopTeams', numTopTeams);
    });
  }.observes('sortedTeams', 'session.isAuthenticated'),
  actions:{
    openTeamView: function(team){
      this.set('modal.team', team);
      this.set('modal.isTeam', true);
    }
  },
});
