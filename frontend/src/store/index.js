import { createStore } from 'vuex';

export default createStore({
    state() {
        var roles = []
        var token = null
        if(sessionStorage.getItem("roles")){
            roles = sessionStorage.getItem("roles")
            token = sessionStorage.getItem("token")
        }
        return{
            roles: roles,
            token: token
        }
    },
    mutations: {
        setRoles(state, value ){
            sessionStorage.setItem("roles", value)
            state.roles = value;
        },
  addRole(state, role) {
    if (!state.roles.includes(role)) {
        state.roles.push(role);
        console.log(role)
        sessionStorage.setItem("roles", JSON.stringify(state.roles));
      }
  },
        setToken(state, token){
            sessionStorage.setItem("token", token)
            state.token = token
        },
        clearSession(state){
            state.roles = []
            state.token = null
            sessionStorage.removeItem("token")
            sessionStorage.removeItem("roles")
        }
    
    },
    getters:{
        getRoles(state){
            console.log(state.roles);
            return state.roles;
        }
    }
})