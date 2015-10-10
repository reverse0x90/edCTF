import Ember from 'ember';

export default Ember.Controller.extend({
  sortedTeams: Ember.computed.sort('content', function(a, b){
    if (a.get('points') < b.get('points')) {
      return 1;
    } else if (a.get('points') > b.get('points')) {
      return -1;
    }
    return 0;
  }),
  numberTopTeams: 0,
  topTeams: [],
  actions:{
    setTopTeams: function(n){
      if (!n){
        n = 10;
      }
      this.set('numberTopTeams', n);
      this.set('topTeams', this.get('sortedTeams').slice(0,n));
    },
  },
});
