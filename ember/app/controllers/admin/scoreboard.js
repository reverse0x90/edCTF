import Ember from 'ember';

export default Ember.Controller.extend({
  settings: {},
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
    changeSelectedCtf: function(ctf){
      this.set('selectedCtf', ctf);
    },
    openTeamView: function(team){
      this.set('modal.team', team);
      //this.set('modal.isAdminTeam', true);
      this.set('modal.isTeam', true);
    }
  },
});
