import Ember from 'ember';

export default Ember.Controller.extend({
  modal: {},
  scoreboard: undefined,
  numberTopTeams: function(){
    return this.get('scoreboard.numtopteams')
  }.property('numberTopTeams'),
  topTeams: undefined,
  options: {
    lineWidth: 0,
    width: 900,
    height: 500,
    //selectionMode: 'multiple',
  },
  teamsChange: function(){
    var teams = this.get('scoreboard.teams');
    if(!teams){
      return
    }

    var numberTopTeams = this.get('scoreboard.numtopteams');
    var topteams = [];

    // x-axis name and team names 
    var teamsNames = [''];

    // temp times along x-axis
    var time1 = ['Time 1'];
    var time2 = ['Time 2'];
    var time3 = ['Time 3'];

    
    // setting top teams
    teams = teams.filter(function(item, index, self) {
      if (index < numberTopTeams){return true}
    });

    // setting y-axis values as points
    teams.forEach(function(team) {
      var max = team.get('points');
      teamsNames.push(team.get('teamname'));
      time1.push(0);
      time2.push(max-Math.floor(Math.random() * (max-100)));
      time3.push(max);
    });

    topteams.push(teamsNames);
    topteams.push(time1);
    topteams.push(time2);
    topteams.push(time3);
    
    this.set('topTeams', topteams);
  }.observes('scoreboard.teams').on('init'),
  actions:{
    setTopTeams: function(n){
      if (!n){
        n = 10;
      }
      this.set('numberTopTeams', n);
      this.set('topTeams', this.get('sortedTeams').slice(0,n));
    },
    openTeamView: function(id){
      this.store.find('team', id).then((team) => {
        this.set('modal.team', team);
      });
      this.set('modal.isTeam', true);
    }
  },
});
