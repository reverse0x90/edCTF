import Ember from 'ember';

export default Ember.Controller.extend({
  init: function () {
    this._super();
    this.set('teams', this.store.findAll('team'), function(){alert();});
    this.set('sortedTeams', Ember.computed.sort('teams', function(a, b){
      if (a.get('points') < b.get('points')) {
        return 1;
      } else if (a.get('points') > b.get('points')) {
        return -1;
      }
      return 0;
    }));
    
    var teams = this.get('sortedTeams');
    var my = this;
    var numberTopTeams = 10
    Ember.run.later(function(){
      console.log(1);
      var topteams = [];
      var top = [''];
      var time1 = ['Time 1'];
      var time2 = ['Time 2'];
      var time3 = ['Time 3'];
      var i = 0;
      teams.forEach(function(team){
        if (i < numberTopTeams){
          var max = team.get('points');
          top.push(team.get('teamname'));
          time1.push(0);
          time2.push(max-Math.floor(Math.random() * (max-100)));
          time3.push(max);
        }
        i++;
      });

      topteams.push(top);
      topteams.push(time1);
      topteams.push(time2);
      topteams.push(time3);

      var options = {
        lineWidth: 0,
        width: 900,
        height: 500,
        //selectionMode: 'multiple',
      };

      my.set('numberTopTeams', numberTopTeams);
      my.set('options', options);
      my.set('topteams', topteams);
    }, 2);
  },
  modal: {},
  numberTopTeams: 0,
  topTeams: [],
  sortedTeams: [],
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
