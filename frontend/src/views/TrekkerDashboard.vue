<template>
  <div class="flex h-screen bg-gray-50 overflow-hidden" style="font-family: 'Inter', sans-serif;">

    <!-- ══════════════ SIDEBAR ══════════════ -->
    <aside class="flex flex-col w-60 shrink-0 bg-green-900 text-white overflow-hidden"
      :class="sidebarOpen ? 'fixed inset-y-0 left-0 z-50' : 'hidden lg:flex'">

      <!-- Logo -->
      <div class="flex items-center gap-3 px-5 py-5 border-b border-green-800">
        <div class="w-9 h-9 bg-green-500 rounded-xl flex items-center justify-center shadow">
          <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M3 17l5-10 4 8 3-5 4 7H3z"/>
          </svg>
        </div>
        <span class="font-bold text-lg" style="font-family:'Poppins',sans-serif">Trek<span class="text-green-300">Hub</span></span>
      </div>

      <!-- Nav -->
      <nav class="flex-1 py-4 px-3 space-y-0.5 overflow-y-auto">
        <button v-for="item in navItems" :key="item.key"
          @click="activeTab = item.key; sidebarOpen = false"
          class="w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium transition-all text-left"
          :class="activeTab === item.key ? 'bg-green-700 text-white' : 'text-green-200 hover:bg-green-800 hover:text-white'">
          <component :is="item.icon" class="w-4 h-4 shrink-0"/>
          {{ item.label }}
          <span v-if="item.key === 'notifications' && unreadCount > 0"
            class="ml-auto bg-red-500 text-white text-xs font-bold rounded-full w-5 h-5 flex items-center justify-center shrink-0">
            {{ unreadCount }}
          </span>
        </button>
      </nav>

      <!-- Motivational quote card -->
      <div class="mx-3 mb-3 p-4 bg-green-800 rounded-2xl relative overflow-hidden">
        <img src="https://images.unsplash.com/photo-1551632811-561732d1e306?w=300&q=60"
          class="absolute inset-0 w-full h-full object-cover opacity-20"/>
        <div class="relative z-10">
          <p class="text-green-100 text-xs leading-relaxed">"The best view comes after the hardest climb."</p>
          <p class="text-green-400 text-xs font-semibold mt-2">Keep exploring!</p>
        </div>
      </div>

      <!-- Logout -->
      <div class="px-3 pb-4">
        <button @click="handleLogout"
          class="w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium text-green-300 hover:bg-green-800 hover:text-white transition-all">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"/>
          </svg>
          Logout
        </button>
      </div>
    </aside>

    <!-- mobile overlay -->
    <div v-if="sidebarOpen" class="fixed inset-0 bg-black/40 z-40 lg:hidden" @click="sidebarOpen = false"></div>

    <!-- ══════════════ MAIN ══════════════ -->
    <div class="flex-1 flex flex-col min-w-0 overflow-hidden">

      <!-- Top bar -->
      <header class="flex items-center px-6 py-3.5 bg-white border-b border-gray-100 shrink-0 shadow-sm">
        <button @click="sidebarOpen = !sidebarOpen" class="lg:hidden p-2 rounded-lg hover:bg-gray-100 text-gray-500 mr-3">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/>
          </svg>
        </button>

        <span class="text-gray-700 font-semibold text-sm hidden lg:block">{{ currentPageTitle }}</span>

        <div class="flex items-center gap-3 ml-auto">
          <!-- Bell -->
          <button @click="activeTab = 'notifications'"
            class="relative p-2 rounded-xl hover:bg-gray-100 text-gray-500 transition-colors">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"/>
            </svg>
            <span v-if="unreadCount > 0"
              class="absolute -top-0.5 -right-0.5 bg-red-500 text-white text-xs font-bold rounded-full w-4 h-4 flex items-center justify-center leading-none">
              {{ unreadCount }}
            </span>
          </button>

          <!-- Role Switcher -->
          <div class="relative" ref="roleSwitcherRef">
            <button @click="showRoleSwitcher = !showRoleSwitcher"
              class="flex items-center gap-2 border border-green-200 bg-green-50 hover:bg-green-100 text-green-700 font-semibold px-3 py-2 rounded-xl text-xs transition-all">
              <span>🔄</span>
              Switch Role
              <svg class="w-3.5 h-3.5 transition-transform" :class="showRoleSwitcher ? 'rotate-180' : ''" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
              </svg>
            </button>
            <div v-if="showRoleSwitcher"
              class="absolute right-0 top-full mt-2 w-64 bg-white border border-gray-200 rounded-2xl shadow-xl z-50 overflow-hidden">
              <div class="px-4 py-2.5 bg-gray-50 border-b border-gray-100">
                <p class="text-xs font-semibold text-gray-400 uppercase tracking-wide">Demo — Switch Dashboard</p>
              </div>
              <div class="divide-y divide-gray-50">
                <button v-for="r in demoRoles" :key="r.role"
                  @click="switchRole(r)"
                  class="w-full flex items-center gap-3 px-4 py-3 hover:bg-green-50 transition-colors text-left group"
                  :class="r.current ? 'bg-green-50' : ''">
                  <span class="w-9 h-9 rounded-xl flex items-center justify-center text-lg shrink-0" :class="r.bg">{{ r.icon }}</span>
                  <div class="flex-1">
                    <p class="text-sm font-semibold text-gray-900">{{ r.label }}</p>
                    <p class="text-xs text-gray-400">{{ r.email }}</p>
                  </div>
                  <span v-if="r.current" class="text-xs font-bold text-green-600 bg-green-100 px-2 py-0.5 rounded-full">Active</span>
                  <span v-if="switchingRole" class="text-xs text-gray-400">...</span>
                </button>
              </div>
            </div>
          </div>

          <!-- User -->
          <div class="flex items-center gap-2.5 pl-3 border-l border-gray-200">
            <div class="w-9 h-9 rounded-full bg-green-700 flex items-center justify-center text-white font-bold text-sm shadow overflow-hidden">
              <img src="https://images.unsplash.com/photo-1633332755192-727a05c4013d?w=80&q=80"
                class="w-full h-full object-cover" :alt="user?.name"/>
            </div>
            <div class="hidden sm:block leading-tight">
              <p class="text-sm font-semibold text-gray-900">{{ user?.name }}</p>
              <p class="text-xs text-gray-400 capitalize">{{ user?.role?.toLowerCase() }}</p>
            </div>
            <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
            </svg>
          </div>
        </div>
      </header>

      <!-- Page content -->
      <main class="flex-1 overflow-y-auto p-6">

        <!-- ─────────── DASHBOARD ─────────── -->
        <div v-show="activeTab === 'dashboard'" class="space-y-6">
          <!-- Welcome -->
          <div>
            <h1 class="text-2xl font-bold text-gray-900" style="font-family:'Poppins',sans-serif">
              Welcome back, {{ user?.name?.split(' ')[0] }}! 👋
            </h1>
            <p class="text-gray-500 text-sm mt-0.5">Here's what's happening with your treks.</p>
          </div>

          <!-- Stat cards — 4 cols matching screenshot -->
          <div class="grid grid-cols-2 lg:grid-cols-4 gap-4">
            <!-- Total Treks Booked -->
            <div class="bg-white rounded-2xl border border-gray-100 p-5 shadow-sm hover:shadow-md transition-shadow">
              <div class="flex items-start justify-between">
                <div>
                  <p class="text-xs text-gray-500 font-medium leading-tight">Total Treks<br>Booked</p>
                  <p class="text-3xl font-black text-gray-900 mt-1.5" style="font-family:'Poppins',sans-serif">{{ bookings.length }}</p>
                  <p class="text-xs text-orange-500 font-medium mt-1">All time</p>
                </div>
                <div class="w-12 h-12 rounded-xl bg-green-100 flex items-center justify-center text-xl">🏔</div>
              </div>
            </div>
            <!-- Upcoming -->
            <div class="bg-white rounded-2xl border border-gray-100 p-5 shadow-sm hover:shadow-md transition-shadow">
              <div class="flex items-start justify-between">
                <div>
                  <p class="text-xs text-gray-500 font-medium">Upcoming Treks</p>
                  <p class="text-3xl font-black text-gray-900 mt-1.5" style="font-family:'Poppins',sans-serif">{{ upcomingBookings.length }}</p>
                  <p class="text-xs text-blue-500 font-medium mt-1">Next 30 days</p>
                </div>
                <div class="w-12 h-12 rounded-xl bg-blue-100 flex items-center justify-center text-xl">📅</div>
              </div>
            </div>
            <!-- Total Spent -->
            <div class="bg-white rounded-2xl border border-gray-100 p-5 shadow-sm hover:shadow-md transition-shadow">
              <div class="flex items-start justify-between">
                <div>
                  <p class="text-xs text-gray-500 font-medium">Total Spent</p>
                  <p class="text-2xl font-black text-gray-900 mt-1.5" style="font-family:'Poppins',sans-serif">₹{{ totalSpent.toLocaleString() }}</p>
                  <p class="text-xs text-orange-500 font-medium mt-1">All time</p>
                </div>
                <div class="w-12 h-12 rounded-xl bg-orange-100 flex items-center justify-center text-xl">💰</div>
              </div>
            </div>
            <!-- Reviews -->
            <div class="bg-white rounded-2xl border border-gray-100 p-5 shadow-sm hover:shadow-md transition-shadow">
              <div class="flex items-start justify-between">
                <div>
                  <p class="text-xs text-gray-500 font-medium">Reviews Given</p>
                  <p class="text-3xl font-black text-gray-900 mt-1.5" style="font-family:'Poppins',sans-serif">{{ completedCount }}</p>
                  <p class="text-xs text-purple-500 font-medium mt-1">All time</p>
                </div>
                <div class="w-12 h-12 rounded-xl bg-purple-100 flex items-center justify-center text-xl">⭐</div>
              </div>
            </div>
          </div>

          <!-- Upcoming Treks + Recent Bookings -->
          <div class="grid lg:grid-cols-2 gap-5">
            <!-- Upcoming -->
            <div class="bg-white rounded-2xl border border-gray-100 shadow-sm p-5">
              <div class="flex items-center justify-between mb-4">
                <h3 class="font-bold text-gray-900 text-base">Upcoming Treks</h3>
                <button @click="activeTab='bookings'" class="text-sm text-green-600 font-semibold hover:text-green-700">View All</button>
              </div>
              <div class="space-y-3">
                <p v-if="upcomingBookings.length === 0" class="text-center py-6 text-gray-400 text-sm">No upcoming treks</p>
                <div v-for="b in upcomingBookings.slice(0,2)" :key="b.id"
                  class="flex gap-3 p-3 rounded-xl border border-gray-100 hover:border-green-200 hover:bg-green-50/50 transition-all">
                  <img :src="getTrekImage(b.trek_name)" :alt="b.trek_name"
                    class="w-20 h-16 rounded-xl object-cover shrink-0"/>
                  <div class="flex-1 min-w-0">
                    <div class="flex items-start justify-between gap-2">
                      <p class="font-bold text-gray-900 text-sm leading-tight">{{ b.trek_name }}</p>
                      <span class="text-xs bg-green-100 text-green-700 font-semibold px-2.5 py-0.5 rounded-full shrink-0 whitespace-nowrap">Confirmed</span>
                    </div>
                    <p class="text-xs text-gray-500 mt-0.5">{{ b.location }}</p>
                    <div class="flex items-center gap-3 mt-1.5 text-xs text-gray-400">
                      <span class="flex items-center gap-1">
                        <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><rect x="3" y="4" width="18" height="18" rx="2" stroke-width="2"/><line x1="16" y1="2" x2="16" y2="6" stroke-width="2" stroke-linecap="round"/><line x1="8" y1="2" x2="8" y2="6" stroke-width="2" stroke-linecap="round"/><line x1="3" y1="10" x2="21" y2="10" stroke-width="2"/></svg>
                        {{ b.start_date }} – {{ b.end_date }}
                      </span>
                      <span class="flex items-center gap-1">
                        <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
                        12 Participants
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Recent Bookings -->
            <div class="bg-white rounded-2xl border border-gray-100 shadow-sm p-5">
              <div class="flex items-center justify-between mb-4">
                <h3 class="font-bold text-gray-900 text-base">Recent Bookings</h3>
                <button @click="activeTab='bookings'" class="text-sm text-green-600 font-semibold hover:text-green-700">View All</button>
              </div>
              <div class="space-y-2.5">
                <p v-if="bookings.length === 0" class="text-center py-6 text-gray-400 text-sm">No bookings yet</p>
                <div v-for="b in bookings.slice(0,3)" :key="b.id"
                  class="flex items-center gap-3 p-2.5 rounded-xl hover:bg-gray-50 transition-all">
                  <img :src="getTrekImage(b.trek_name)" :alt="b.trek_name"
                    class="w-14 h-12 rounded-xl object-cover shrink-0"/>
                  <div class="flex-1 min-w-0">
                    <p class="font-semibold text-gray-900 text-sm truncate">{{ b.trek_name }}</p>
                    <p class="text-xs text-gray-400 mt-0.5">{{ b.location }} · {{ b.start_date }}</p>
                  </div>
                  <div class="text-right shrink-0">
                    <p class="text-sm font-bold text-gray-800">₹{{ getRandomPrice(b.trek_name) }}</p>
                    <p class="text-xs font-semibold mt-0.5"
                      :class="b.booking_status==='Completed' ? 'text-green-600' : b.booking_status==='Booked' ? 'text-blue-600' : 'text-red-500'">
                      {{ b.booking_status }}
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Charts row + Quick Actions -->
          <div class="grid lg:grid-cols-3 gap-5">
            <!-- Line chart: Bookings Overview -->
            <div class="bg-white rounded-2xl border border-gray-100 shadow-sm p-5 lg:col-span-1">
              <div class="flex items-center justify-between mb-4">
                <h3 class="font-bold text-gray-900 text-base">Bookings Overview</h3>
                <select class="text-xs border border-gray-200 rounded-lg px-2.5 py-1.5 text-gray-600 focus:outline-none focus:ring-1 focus:ring-green-500">
                  <option>Last 6 Months</option>
                  <option>Last Year</option>
                </select>
              </div>
              <div class="relative" style="height:180px">
                <canvas ref="lineChartRef" style="width:100%;height:100%"></canvas>
              </div>
            </div>

            <!-- Donut chart: Bookings by Status -->
            <div class="bg-white rounded-2xl border border-gray-100 shadow-sm p-5">
              <h3 class="font-bold text-gray-900 text-base mb-4">Bookings by Status</h3>
              <div class="flex items-center gap-4">
                <div class="relative shrink-0" style="width:120px;height:120px">
                  <canvas ref="donutChartRef" style="width:120px;height:120px"></canvas>
                  <div class="absolute inset-0 flex flex-col items-center justify-center pointer-events-none">
                    <span class="text-xs text-gray-500 font-medium">Total</span>
                    <span class="text-xl font-black text-gray-900">{{ bookings.length }}</span>
                  </div>
                </div>
                <div class="space-y-2 flex-1">
                  <div class="flex items-center justify-between text-xs">
                    <span class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded-full bg-green-500 inline-block"></span> Completed</span>
                    <span class="font-semibold text-gray-700">{{ completedCount }} ({{ bookings.length ? Math.round(completedCount/bookings.length*100) : 0 }}%)</span>
                  </div>
                  <div class="flex items-center justify-between text-xs">
                    <span class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded-full bg-blue-500 inline-block"></span> Upcoming</span>
                    <span class="font-semibold text-gray-700">{{ upcomingBookings.length }} ({{ bookings.length ? Math.round(upcomingBookings.length/bookings.length*100) : 0 }}%)</span>
                  </div>
                  <div class="flex items-center justify-between text-xs">
                    <span class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded-full bg-yellow-400 inline-block"></span> Cancelled</span>
                    <span class="font-semibold text-gray-700">{{ cancelledCount }} ({{ bookings.length ? Math.round(cancelledCount/bookings.length*100) : 0 }}%)</span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Quick Actions -->
            <div class="bg-white rounded-2xl border border-gray-100 shadow-sm p-5">
              <h3 class="font-bold text-gray-900 text-base mb-4">Quick Actions</h3>
              <div class="space-y-2">
                <button v-for="qa in quickActions" :key="qa.label"
                  @click="activeTab = qa.tab"
                  class="w-full flex items-center justify-between px-3.5 py-2.5 rounded-xl border border-gray-100 hover:border-green-300 hover:bg-green-50 transition-all text-sm font-medium text-gray-700 hover:text-green-700 group">
                  <span class="flex items-center gap-2.5">
                    <span class="w-7 h-7 rounded-lg bg-gray-100 group-hover:bg-green-100 flex items-center justify-center text-base transition-colors">{{ qa.icon }}</span>
                    {{ qa.label }}
                  </span>
                  <svg class="w-3.5 h-3.5 text-gray-300 group-hover:text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
                  </svg>
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- ─────────── BROWSE TREKS ─────────── -->
        <div v-show="activeTab === 'browse'" class="space-y-5">
          <h1 class="text-xl font-bold text-gray-900" style="font-family:'Poppins',sans-serif">Browse Treks</h1>

          <div class="bg-white rounded-2xl border border-gray-100 shadow-sm p-4">
            <div class="grid grid-cols-2 lg:grid-cols-4 gap-3 items-end">
              <div>
                <label class="text-xs font-semibold text-gray-400 uppercase tracking-wide block mb-1.5">Location</label>
                <input type="text" v-model="filters.location" placeholder="e.g. Himalayas"
                  class="w-full px-3 py-2.5 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-green-500 bg-gray-50 focus:bg-white transition-all"/>
              </div>
              <div>
                <label class="text-xs font-semibold text-gray-400 uppercase tracking-wide block mb-1.5">Difficulty</label>
                <select v-model="filters.difficulty"
                  class="w-full px-3 py-2.5 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-green-500 bg-gray-50 focus:bg-white transition-all">
                  <option value="">All levels</option>
                  <option>Easy</option><option>Moderate</option><option>Hard</option>
                </select>
              </div>
              <div>
                <label class="text-xs font-semibold text-gray-400 uppercase tracking-wide block mb-1.5">Duration (days)</label>
                <input type="number" v-model="filters.duration_days" placeholder="e.g. 7"
                  class="w-full px-3 py-2.5 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-green-500 bg-gray-50 focus:bg-white transition-all"/>
              </div>
              <button @click="applyFilters"
                class="flex items-center justify-center gap-2 bg-green-700 hover:bg-green-800 text-white font-semibold py-2.5 rounded-xl text-sm transition-all shadow-sm">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-4.35-4.35M17 11A6 6 0 115 11a6 6 0 0112 0z"/>
                </svg>
                Apply Filters
              </button>
            </div>
          </div>

          <div class="grid sm:grid-cols-2 xl:grid-cols-3 gap-5">
            <div v-for="t in openTreks" :key="t.id"
              class="bg-white rounded-2xl border border-gray-100 shadow-sm hover:shadow-lg hover:-translate-y-1 transition-all duration-200 overflow-hidden group">
              <div class="relative h-44 overflow-hidden">
                <img :src="getTrekImage(t.trek_name)" :alt="t.trek_name"
                  class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"/>
                <div class="absolute inset-0 bg-gradient-to-t from-black/50 to-transparent"></div>
                <span class="absolute top-3 right-3 text-xs font-bold px-2.5 py-1 rounded-full"
                  :class="t.difficulty==='Easy' ? 'bg-green-500 text-white' : t.difficulty==='Moderate' ? 'bg-yellow-500 text-white' : 'bg-red-500 text-white'">
                  {{ t.difficulty }}
                </span>
                <span class="absolute bottom-3 left-3 text-white text-xs font-semibold">📍 {{ t.location }}</span>
              </div>
              <div class="p-4">
                <h3 class="font-bold text-gray-900 mb-1">{{ t.trek_name }}</h3>
                <div class="flex gap-3 text-xs text-gray-500 mb-3">
                  <span>📅 {{ t.start_date }}</span>
                  <span>⏱ {{ t.duration_days }} days</span>
                </div>
                <div class="mb-3">
                  <div class="flex justify-between text-xs text-gray-400 mb-1">
                    <span>Slots available</span>
                    <span class="font-semibold text-gray-700">{{ t.available_slots }}/{{ t.max_participants }}</span>
                  </div>
                  <div class="h-1.5 bg-gray-100 rounded-full overflow-hidden">
                    <div class="h-full bg-green-500 rounded-full"
                      :style="{width: ((t.max_participants - t.available_slots) / t.max_participants * 100) + '%'}"></div>
                  </div>
                </div>
                <div class="flex items-center justify-between">
                  <span class="text-green-700 font-bold text-sm">₹{{ t.price?.toLocaleString() }}</span>
                  <button @click="openBookingModal(t)" :disabled="t.available_slots === 0"
                    class="flex items-center gap-1.5 bg-green-700 hover:bg-green-800 disabled:bg-gray-300 text-white text-xs font-semibold px-4 py-2 rounded-xl transition-all">
                    {{ t.available_slots === 0 ? 'Full' : 'Book Now' }}
                  </button>
                </div>
              </div>
            </div>
            <div v-if="openTreks.length === 0"
              class="col-span-full flex flex-col items-center justify-center py-20 text-gray-400">
              <span class="text-4xl mb-3">🏔</span>
              <p class="font-medium">No treks found</p>
              <p class="text-sm">Try adjusting your filters</p>
            </div>
          </div>
        </div>

        <!-- ─────────── MY BOOKINGS ─────────── -->
        <div v-show="activeTab === 'bookings'" class="space-y-5">
          <div class="flex items-center justify-between">
            <h1 class="text-xl font-bold text-gray-900" style="font-family:'Poppins',sans-serif">My Bookings</h1>
            <button @click="exportHistory"
              class="flex items-center gap-2 text-sm border border-gray-200 text-gray-600 hover:border-green-500 hover:text-green-700 px-4 py-2 rounded-xl transition-all font-medium">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
              </svg>
              Export
            </button>
          </div>
          <div class="bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden">
            <table class="w-full text-sm">
              <thead>
                <tr class="bg-gray-50 border-b border-gray-100">
                  <th class="text-left px-5 py-3.5 text-xs font-semibold text-gray-500 uppercase tracking-wide">Trek</th>
                  <th class="text-left px-5 py-3.5 text-xs font-semibold text-gray-500 uppercase tracking-wide hidden md:table-cell">Location</th>
                  <th class="text-left px-5 py-3.5 text-xs font-semibold text-gray-500 uppercase tracking-wide hidden md:table-cell">Dates</th>
                  <th class="text-left px-5 py-3.5 text-xs font-semibold text-gray-500 uppercase tracking-wide">Status</th>
                  <th class="text-left px-5 py-3.5 text-xs font-semibold text-gray-500 uppercase tracking-wide hidden lg:table-cell">Payment</th>
                  <th class="px-5 py-3.5"></th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-50">
                <tr v-for="b in bookings" :key="b.id" class="hover:bg-gray-50 transition-colors">
                  <td class="px-5 py-3.5 font-semibold text-gray-900">{{ b.trek_name }}</td>
                  <td class="px-5 py-3.5 text-gray-500 hidden md:table-cell">{{ b.location }}</td>
                  <td class="px-5 py-3.5 text-gray-400 text-xs hidden md:table-cell">{{ b.start_date }} → {{ b.end_date }}</td>
                  <td class="px-5 py-3.5">
                    <span class="inline-flex px-2.5 py-1 rounded-full text-xs font-semibold"
                      :class="b.booking_status==='Booked' ? 'bg-green-100 text-green-700' : b.booking_status==='Completed' ? 'bg-gray-100 text-gray-600' : 'bg-red-100 text-red-600'">
                      {{ b.booking_status }}
                    </span>
                  </td>
                  <td class="px-5 py-3.5 hidden lg:table-cell">
                    <span class="inline-flex px-2.5 py-1 rounded-full text-xs font-semibold"
                      :class="b.payment_status==='Paid' ? 'bg-green-100 text-green-700' : b.payment_status==='Pending' ? 'bg-yellow-100 text-yellow-700' : 'bg-red-100 text-red-600'">
                      {{ b.payment_status }}
                    </span>
                  </td>
                  <td class="px-5 py-3.5">
                    <button v-if="b.booking_status==='Booked'" @click="cancelBooking(b.id)"
                      class="text-xs font-semibold text-red-500 hover:text-red-700 border border-red-200 hover:border-red-400 px-3 py-1.5 rounded-lg transition-all">
                      Cancel
                    </button>
                    <span v-else class="text-gray-300">—</span>
                  </td>
                </tr>
                <tr v-if="bookings.length === 0">
                  <td colspan="6" class="text-center py-16 text-gray-400">
                    <span class="text-3xl block mb-2">📋</span>No booking records yet.
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- ─────────── NOTIFICATIONS ─────────── -->
        <div v-show="activeTab === 'notifications'" class="space-y-5">
          <h1 class="text-xl font-bold text-gray-900" style="font-family:'Poppins',sans-serif">Notifications</h1>
          <div class="bg-white rounded-2xl border border-gray-100 shadow-sm divide-y divide-gray-50">
            <div v-if="notifications.length === 0" class="text-center py-16 text-gray-400">
              <span class="text-3xl block mb-2">🔔</span>No notifications yet.
            </div>
            <div v-for="n in notifications" :key="n.id"
              class="flex items-start gap-4 px-5 py-4 hover:bg-gray-50 transition-colors"
              :class="{'bg-green-50/50': !n.is_read}">
              <div class="w-9 h-9 rounded-xl flex items-center justify-center shrink-0"
                :class="n.is_read ? 'bg-gray-100' : 'bg-green-100'">
                <span class="text-sm">{{ n.is_read ? '📬' : '🔔' }}</span>
              </div>
              <div class="flex-1 min-w-0">
                <p class="text-sm text-gray-800" v-html="n.message"></p>
                <p class="text-xs text-gray-400 mt-1">{{ n.created_at }}</p>
              </div>
              <button v-if="!n.is_read" @click="markRead(n.id)"
                class="text-xs text-green-600 font-semibold hover:text-green-700 shrink-0">Mark read</button>
            </div>
          </div>
        </div>

        <!-- ─────────── PROFILE ─────────── -->
        <div v-show="activeTab === 'profile'" class="space-y-5 max-w-2xl">
          <h1 class="text-xl font-bold text-gray-900" style="font-family:'Poppins',sans-serif">My Profile</h1>
          <div class="bg-white rounded-2xl border border-gray-100 shadow-sm p-6 space-y-5">
            <div class="flex items-center gap-4 pb-5 border-b border-gray-100">
              <div class="w-16 h-16 rounded-2xl bg-green-700 flex items-center justify-center text-white font-black text-2xl shadow overflow-hidden">
                <img src="https://images.unsplash.com/photo-1633332755192-727a05c4013d?w=100&q=80" class="w-full h-full object-cover" :alt="user?.name"/>
              </div>
              <div>
                <p class="font-bold text-gray-900 text-lg">{{ user?.name }}</p>
                <p class="text-sm text-gray-400">{{ user?.email }}</p>
                <span class="text-xs bg-green-100 text-green-700 font-semibold px-2 py-0.5 rounded-full mt-1 inline-block capitalize">{{ user?.role?.toLowerCase() }}</span>
              </div>
            </div>
            <form @submit.prevent="updateProfile" class="space-y-4">
              <h3 class="font-semibold text-gray-800">Update Profile</h3>
              <div class="grid grid-cols-2 gap-4">
                <div class="space-y-1.5">
                  <label class="text-xs font-semibold text-gray-400 uppercase tracking-wide">Full Name</label>
                  <input type="text" v-model="profileForm.name" required
                    class="w-full px-3 py-2.5 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-green-500 bg-gray-50 focus:bg-white transition-all"/>
                </div>
                <div class="space-y-1.5">
                  <label class="text-xs font-semibold text-gray-400 uppercase tracking-wide">Phone</label>
                  <input type="text" v-model="profileForm.phone"
                    class="w-full px-3 py-2.5 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-green-500 bg-gray-50 focus:bg-white transition-all"/>
                </div>
              </div>
              <button type="submit"
                class="flex items-center gap-2 bg-green-700 hover:bg-green-800 text-white font-semibold px-5 py-2.5 rounded-xl text-sm transition-all shadow-sm">
                Save Changes
              </button>
            </form>
          </div>
          <div class="bg-white rounded-2xl border border-gray-100 shadow-sm p-6 space-y-4">
            <h3 class="font-semibold text-gray-800">Change Password</h3>
            <form @submit.prevent="resetPassword" class="space-y-4">
              <div class="space-y-1.5">
                <label class="text-xs font-semibold text-gray-400 uppercase tracking-wide">Email</label>
                <input type="email" v-model="passwordResetForm.email" disabled
                  class="w-full px-3 py-2.5 border border-gray-200 rounded-xl text-sm bg-gray-100 text-gray-500"/>
              </div>
              <div class="space-y-1.5">
                <label class="text-xs font-semibold text-gray-400 uppercase tracking-wide">New Password</label>
                <input type="password" v-model="passwordResetForm.new_password" required placeholder="Minimum 6 characters"
                  class="w-full px-3 py-2.5 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-green-500 bg-gray-50 focus:bg-white transition-all"/>
              </div>
              <button type="submit"
                class="border border-gray-300 hover:border-green-500 text-gray-700 hover:text-green-700 font-semibold px-5 py-2.5 rounded-xl text-sm transition-all">
                Update Password
              </button>
            </form>
          </div>
        </div>

      </main>
    </div>

    <!-- ══════════════ BOOKING MODAL ══════════════ -->
    <div v-if="showBookingModal"
      class="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4"
      @click.self="showBookingModal = false">
      <div class="bg-white rounded-2xl shadow-2xl w-full max-w-md modal-animate">
        <div class="flex items-center justify-between px-6 py-4 border-b border-gray-100">
          <h3 class="font-bold text-gray-900">Confirm Booking</h3>
          <button @click="showBookingModal = false"
            class="w-8 h-8 flex items-center justify-center rounded-xl hover:bg-gray-100 text-gray-400 transition-all">✕</button>
        </div>
        <form @submit.prevent="confirmBooking">
          <div class="p-6 space-y-4">
            <div class="flex gap-3 p-3 bg-green-50 rounded-xl border border-green-100">
              <img :src="getTrekImage(selectedTrek?.trek_name)" class="w-14 h-14 rounded-xl object-cover shrink-0"/>
              <div>
                <p class="font-bold text-gray-900 text-sm">{{ selectedTrek?.trek_name }}</p>
                <p class="text-xs text-gray-500 mt-0.5">{{ selectedTrek?.location }}</p>
                <p class="text-xs text-green-700 font-semibold mt-1">₹{{ selectedTrek?.price?.toLocaleString() }}</p>
              </div>
            </div>
            <div class="space-y-1.5">
              <label class="text-xs font-semibold text-gray-400 uppercase tracking-wide">Remarks / Special Requests</label>
              <textarea v-model="bookingRemarks" rows="3" placeholder="Dietary needs, medical info, notes..."
                class="w-full px-3 py-2.5 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-green-500 bg-gray-50 focus:bg-white transition-all resize-none"></textarea>
            </div>
          </div>
          <div class="flex gap-3 px-6 pb-5">
            <button type="button" @click="showBookingModal = false"
              class="flex-1 border border-gray-200 text-gray-600 font-semibold py-2.5 rounded-xl hover:bg-gray-50 text-sm transition-all">
              Cancel
            </button>
            <button type="submit"
              class="flex-1 bg-green-700 hover:bg-green-800 text-white font-semibold py-2.5 rounded-xl text-sm transition-all shadow-sm">
              Confirm Booking
            </button>
          </div>
        </form>
      </div>
    </div>

  </div>
</template>

<script>
import { ref, computed, onMounted, onBeforeUnmount, reactive, watch, nextTick } from 'vue';
import { useRouter } from 'vue-router';
import { Chart, LineElement, PointElement, LineController, CategoryScale, LinearScale, Filler, Tooltip, ArcElement, DoughnutController } from 'chart.js';
import api from '../services/api';
import store from '../store';

const DEMO_CREDS = {
  TREKKER: { email: 'trekker@tma.com', password: 'pass123' },
  STAFF:   { email: 'staff@tma.com',   password: 'pass123' },
  ADMIN:   { email: 'admin@tma.com',   password: 'pass123' },
};

Chart.register(LineElement, PointElement, LineController, CategoryScale, LinearScale, Filler, Tooltip, ArcElement, DoughnutController);

const TREK_IMAGES = [
  'https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=400&q=80',
  'https://images.unsplash.com/photo-1551632811-561732d1e306?w=400&q=80',
  'https://images.unsplash.com/photo-1486870591958-9b9d0d1dda99?w=400&q=80',
  'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400&q=80',
  'https://images.unsplash.com/photo-1519681393784-d120267933ba?w=400&q=80',
  'https://images.unsplash.com/photo-1434394354979-a235cd36269d?w=400&q=80',
];

const PRICES = [3950, 5450, 6250, 7800, 4500, 8200, 5900, 6700];

function getTrekImage(name) {
  if (!name) return TREK_IMAGES[0];
  let h = 0;
  for (let i = 0; i < name.length; i++) h = (h * 31 + name.charCodeAt(i)) & 0xffffffff;
  return TREK_IMAGES[Math.abs(h) % TREK_IMAGES.length];
}

function getRandomPrice(name) {
  if (!name) return PRICES[0];
  let h = 0;
  for (let i = 0; i < name.length; i++) h = (h * 31 + name.charCodeAt(i)) & 0xffffffff;
  return PRICES[Math.abs(h) % PRICES.length].toLocaleString();
}

// SVG icon components as inline render functions
const IconHome = { template: `<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/></svg>` };
const IconMap  = { template: `<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7"/></svg>` };
const IconCalendar = { template: `<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><rect x="3" y="4" width="18" height="18" rx="2" stroke-width="2"/><line x1="16" y1="2" x2="16" y2="6" stroke-width="2" stroke-linecap="round"/><line x1="8" y1="2" x2="8" y2="6" stroke-width="2" stroke-linecap="round"/><line x1="3" y1="10" x2="21" y2="10" stroke-width="2"/></svg>` };
const IconUser  = { template: `<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/></svg>` };
const IconBell  = { template: `<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"/></svg>` };
const IconStar  = { template: `<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z"/></svg>` };
const IconCash  = { template: `<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z"/></svg>` };
const IconDoc   = { template: `<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>` };
const IconSupport = { template: `<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18.364 5.636l-3.536 3.536m0 5.656l3.536 3.536M9.172 9.172L5.636 5.636m3.536 9.192l-3.536 3.536M21 12a9 9 0 11-18 0 9 9 0 0118 0zm-5 0a4 4 0 11-8 0 4 4 0 018 0z"/></svg>` };

export default {
  components: { IconHome, IconMap, IconCalendar, IconUser, IconBell, IconStar, IconCash, IconDoc, IconSupport },
  setup() {
    const router = useRouter();
    const activeTab = ref('dashboard');
    const sidebarOpen = ref(false);
    const showRoleSwitcher = ref(false);
    const switchingRole = ref(false);
    const roleSwitcherRef = ref(null);

    const demoRoles = computed(() => [
      { role: 'TREKKER', label: 'Trekker',  email: 'trekker@tma.com', icon: '🥾', bg: 'bg-green-100',  current: user.value?.role === 'TREKKER' },
      { role: 'STAFF',   label: 'Staff',    email: 'staff@tma.com',   icon: '🧑‍💼', bg: 'bg-orange-100', current: user.value?.role === 'STAFF'   },
      { role: 'ADMIN',   label: 'Admin',    email: 'admin@tma.com',   icon: '🛡',  bg: 'bg-red-100',    current: user.value?.role === 'ADMIN'   },
    ]);

    const switchRole = async (r) => {
      if (r.current || switchingRole.value) return;
      switchingRole.value = true;
      showRoleSwitcher.value = false;
      try {
        const creds = DEMO_CREDS[r.role];
        const res = await api.post('/api/auth/login', creds);
        store.login(res.data.user, res.data.access_token, res.data.refresh_token);
        if (r.role === 'ADMIN')  router.push({ name: 'AdminDashboard' });
        else if (r.role === 'STAFF') router.push({ name: 'StaffDashboard' });
        else router.push({ name: 'TrekkerDashboard' });
      } catch (e) {
        window.triggerToast('Failed to switch role', 'error');
      } finally {
        switchingRole.value = false;
      }
    };

    // Close dropdown when clicking outside
    const handleClickOutside = (e) => {
      if (roleSwitcherRef.value && !roleSwitcherRef.value.contains(e.target)) {
        showRoleSwitcher.value = false;
      }
    };
    const openTreks = ref([]);
    const bookings = ref([]);
    const notifications = ref([]);
    const selectedTrek = ref(null);
    const bookingRemarks = ref('');
    const showBookingModal = ref(false);
    const lineChartRef = ref(null);
    const donutChartRef = ref(null);
    let lineChart = null;
    let donutChart = null;

    const filters = reactive({ location: '', difficulty: '', duration_days: '', start_date: '' });
    const profileForm = reactive({ name: store.state.user?.name || '', phone: store.state.user?.phone || '' });
    const passwordResetForm = reactive({ email: store.state.user?.email || '', new_password: '' });

    const user = computed(() => store.state.user);
    const unreadCount = computed(() => notifications.value.filter(n => !n.is_read).length);
    const upcomingBookings = computed(() => bookings.value.filter(b => b.booking_status === 'Booked'));
    const completedCount = computed(() => bookings.value.filter(b => b.booking_status === 'Completed').length);
    const cancelledCount = computed(() => bookings.value.filter(b => b.booking_status === 'Cancelled').length);
    const totalSpent = computed(() => {
      let total = 0;
      bookings.value.forEach(b => {
        let h = 0;
        const n = b.trek_name || '';
        for (let i = 0; i < n.length; i++) h = (h * 31 + n.charCodeAt(i)) & 0xffffffff;
        total += PRICES[Math.abs(h) % PRICES.length];
      });
      return total;
    });

    const navItems = [
      { key: 'dashboard',     label: 'Dashboard',    icon: 'IconHome' },
      { key: 'browse',        label: 'Browse Treks', icon: 'IconMap' },
      { key: 'bookings',      label: 'My Bookings',  icon: 'IconCalendar' },
      { key: 'profile',       label: 'My Profile',   icon: 'IconUser' },
      { key: 'notifications', label: 'Notifications',icon: 'IconBell' },
      { key: 'reviews',       label: 'My Reviews',   icon: 'IconStar' },
      { key: 'payments',      label: 'Payments',     icon: 'IconCash' },
      { key: 'documents',     label: 'Documents',    icon: 'IconDoc' },
      { key: 'support',       label: 'Support',      icon: 'IconSupport' },
    ];

    const quickActions = [
      { label: 'Browse Treks',      icon: '🗺', tab: 'browse' },
      { label: 'My Bookings',       icon: '📋', tab: 'bookings' },
      { label: 'Upload Documents',  icon: '📄', tab: 'documents' },
      { label: 'Contact Support',   icon: '🎧', tab: 'support' },
    ];

    const currentPageTitle = computed(() => navItems.find(i => i.key === activeTab.value)?.label || 'Dashboard');

    // Build/update charts
    const buildCharts = () => {
      nextTick(() => {
        // Line chart
        if (lineChartRef.value) {
          if (lineChart) lineChart.destroy();
          lineChart = new Chart(lineChartRef.value, {
            type: 'line',
            data: {
              labels: ['Jan','Feb','Mar','Apr','May','Jun'],
              datasets: [{
                data: [2, 3, 4.5, 4, 6, bookings.value.length || 8],
                borderColor: '#16a34a',
                backgroundColor: 'rgba(22,163,74,0.08)',
                fill: true,
                tension: 0.4,
                pointBackgroundColor: '#16a34a',
                pointRadius: 4,
                pointHoverRadius: 6,
                borderWidth: 2,
              }]
            },
            options: {
              responsive: true, maintainAspectRatio: false,
              plugins: { legend: { display: false }, tooltip: { backgroundColor: '#1f2937', titleColor: '#f9fafb', bodyColor: '#d1fae5' } },
              scales: {
                x: { grid: { display: false }, ticks: { color: '#9ca3af', font: { size: 11 } } },
                y: { grid: { color: '#f3f4f6' }, ticks: { color: '#9ca3af', font: { size: 11 }, stepSize: 2 }, beginAtZero: true },
              },
            }
          });
        }
        // Donut chart
        if (donutChartRef.value) {
          if (donutChart) donutChart.destroy();
          const total = bookings.value.length || 1;
          donutChart = new Chart(donutChartRef.value, {
            type: 'doughnut',
            data: {
              datasets: [{
                data: [completedCount.value || 5, upcomingBookings.value.length || 2, cancelledCount.value || 1],
                backgroundColor: ['#22c55e','#3b82f6','#facc15'],
                borderWidth: 0,
                hoverOffset: 4,
              }]
            },
            options: {
              responsive: false, cutout: '72%',
              plugins: { legend: { display: false }, tooltip: { callbacks: { label: ctx => ` ${ctx.raw} bookings` } } },
            }
          });
        }
      });
    };

    // Re-build donut when bookings change
    watch(bookings, () => buildCharts(), { deep: true });
    watch(() => activeTab.value, (v) => { if (v === 'dashboard') buildCharts(); });

    const loadOpenTreks = async () => {
      try {
        const params = {};
        if (filters.location) params.location = filters.location;
        if (filters.difficulty) params.difficulty = filters.difficulty;
        if (filters.duration_days) params.duration_days = filters.duration_days;
        if (filters.start_date) params.start_date = filters.start_date;
        const res = await api.get('/api/treks', { params });
        openTreks.value = res.data;
      } catch (e) { console.error(e); }
    };

    const loadBookings = async () => {
      try {
        const res = await api.get('/api/trekker/bookings');
        bookings.value = res.data;
      } catch (e) { console.error(e); }
    };

    const loadNotifications = async () => {
      try {
        const res = await api.get('/api/trekker/notifications');
        notifications.value = res.data;
      } catch (e) { console.error(e); }
    };

    const markRead = async (id) => {
      try {
        await api.post(`/api/trekker/notifications/${id}/read`);
        const n = notifications.value.find(x => x.id === id);
        if (n) n.is_read = true;
      } catch (e) { console.error(e); }
    };

    const applyFilters = () => loadOpenTreks();

    const openBookingModal = (trek) => {
      selectedTrek.value = trek; bookingRemarks.value = ''; showBookingModal.value = true;
    };

    const confirmBooking = async () => {
      try {
        await api.post(`/api/trekker/book/${selectedTrek.value.id}`, { remarks: bookingRemarks.value });
        window.triggerToast('Booking confirmed!', 'success');
        showBookingModal.value = false;
        loadOpenTreks(); loadBookings();
      } catch (e) { window.triggerToast(e.response?.data?.error || 'Booking failed', 'error'); }
    };

    const cancelBooking = async (id) => {
      if (!confirm('Cancel this booking?')) return;
      try {
        await api.post(`/api/trekker/cancel/${id}`);
        window.triggerToast('Booking cancelled', 'success');
        loadOpenTreks(); loadBookings();
      } catch (e) { window.triggerToast(e.response?.data?.error || 'Failed', 'error'); }
    };

    const updateProfile = async () => {
      try {
        await api.put('/api/trekker/profile', profileForm);
        store.updateUser(profileForm.name, profileForm.phone);
        window.triggerToast('Profile updated!', 'success');
      } catch (e) { window.triggerToast('Failed to update profile', 'error'); }
    };

    const resetPassword = async () => {
      try {
        await api.post('/api/auth/reset-password', passwordResetForm);
        window.triggerToast('Password updated!', 'success');
        passwordResetForm.new_password = '';
      } catch (e) { window.triggerToast('Failed', 'error'); }
    };

    const exportHistory = async () => {
      try {
        await api.post('/api/trekker/export-history');
        window.triggerToast('Export triggered. You will be notified when ready.', 'success');
      } catch (e) { window.triggerToast('Export failed', 'error'); }
    };

    const handleLogout = () => { store.logout(); router.push({ name: 'Login' }); };

    let pollInterval = null;
    onMounted(async () => {
      await loadOpenTreks();
      await loadBookings();
      await loadNotifications();
      buildCharts();
      document.addEventListener('click', handleClickOutside);
      pollInterval = setInterval(() => {
        loadOpenTreks(); loadBookings(); loadNotifications();
      }, 15000);
    });
    onBeforeUnmount(() => {
      if (pollInterval) clearInterval(pollInterval);
      if (lineChart) lineChart.destroy();
      if (donutChart) donutChart.destroy();
      document.removeEventListener('click', handleClickOutside);
    });

    return {
      activeTab, sidebarOpen, showRoleSwitcher, switchingRole, roleSwitcherRef, demoRoles, switchRole,
      openTreks, bookings, notifications, selectedTrek,
      bookingRemarks, showBookingModal, lineChartRef, donutChartRef,
      filters, profileForm, passwordResetForm,
      user, unreadCount, upcomingBookings, completedCount, cancelledCount, totalSpent,
      navItems, quickActions, currentPageTitle,
      getTrekImage, getRandomPrice, applyFilters, openBookingModal, confirmBooking,
      cancelBooking, updateProfile, resetPassword, exportHistory, markRead, handleLogout,
    };
  }
};
</script>

<style scoped>
.modal-animate {
  animation: modalIn 0.2s cubic-bezier(0.34, 1.56, 0.64, 1) both;
}
@keyframes modalIn {
  from { opacity: 0; transform: scale(0.95) translateY(8px); }
  to   { opacity: 1; transform: scale(1) translateY(0); }
}
</style>
