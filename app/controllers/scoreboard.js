import Ember from 'ember';

export default Ember.Controller.extend({
  modal: {},
  ctf: null,
  c3Options: {
    axis: {
      x: {
        tick: {
          fit: true,
          format: '%Y-%m-%d',
          outer: false,
        },
        type: 'timeseries',
      },
      y: {
        //show: false,
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
  },
  actions:{
    openTeamView: function(id){
      this.store.find('team', id).then((team) => {
        this.set('modal.team', team);
      });
      this.set('modal.isTeam', true);
    }
  },
});
