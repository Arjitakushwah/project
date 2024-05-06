<template>
    <nav class="navbar navbar-light bg-light">
      <div class="container-fluid">
        <a class="navbar-brand">Music Streaming App</a>
        <ul class="nav justify-content-end">
        <li class="nav-item">
            <router-link to="/login" class="nav-link">Login</router-link>
        </li>
        <li class="nav-item">
            <router-link to="/Register" class="nav-link">Register</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/" class="nav-link">Home</router-link>
          </li>
        </ul>
      </div>
    </nav>
  </template>