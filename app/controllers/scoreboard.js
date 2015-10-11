import Ember from 'ember';

export default Ember.Controller.extend({
  modal: {},
  numberTopTeams: 0,
  topTeams: [],
  sortedTeams: Ember.computed.sort('teams', function(a, b){
    if (a.get('points') < b.get('points')) {
      return 1;
    } else if (a.get('points') > b.get('points')) {
      return -1;
    }
    return 0;
  }),
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
