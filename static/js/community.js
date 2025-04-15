const input = document.getElementById('search-input');
const clearBtn = document.getElementById('clear-button');

input.addEventListener('input', () => {
  clearBtn.style.display = input.value ? 'block' : 'none';
});

clearBtn.addEventListener('click', () => {
  input.value = '';
  clearBtn.style.display = 'none';
  input.focus();
});


//11:05
// Nav buttons scroll functionality
document.addEventListener('DOMContentLoaded', function() {
const navButtons = document.querySelectorAll('.nav-btns');

// Map button text to section IDs
const sectionMap = {
    'Featured': 'featured-communities', // You'll need to add id="featured-communities" to your Featured section
    'Open Source': 'open-source-projects', // Add id="open-source-projects" to Open Source section
    'Collaborators Map': 'collaborators-map', // Already has id
    'Upcoming': 'upcoming-events', // Already has id
    'Leaderboard': 'hall-of-impact' // Already has id
};

navButtons.forEach(btn => {
    btn.addEventListener('click', function() {
        // Remove active class from all buttons
        navButtons.forEach(b => b.classList.remove('active'));
        // Add active class to clicked button
        this.classList.add('active');
        
        // Get the section to scroll to
        const sectionName = this.textContent.trim();
        const sectionId = sectionMap[sectionName];
        
        if (sectionId) {
            const section = document.getElementById(sectionId);
            if (section) {
                section.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        }
    });
});
});

//9:43
// Add smooth scrolling to all links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
anchor.addEventListener('click', function (e) {
e.preventDefault();
document.querySelector(this.getAttribute('href')).scrollIntoView({
  behavior: 'smooth'
});
});
});

// Add animation to cards when they come into view
const observer = new IntersectionObserver((entries) => {
entries.forEach(entry => {
if (entry.isIntersecting) {
  entry.target.classList.add('animate__animated', 'animate__fadeInUp');
  observer.unobserve(entry.target);
}
});
}, { threshold: 0.1 });

document.querySelectorAll('.card').forEach(card => {
observer.observe(card);
});


//9:53
// Add this to your existing script section
document.addEventListener('DOMContentLoaded', function() {
// Add click animation to project cards
const projectCards = document.querySelectorAll('.card');

projectCards.forEach(card => {
card.addEventListener('click', function(e) {
  // Don't trigger if clicking on a link inside the card
  if (e.target.tagName === 'A' || e.target.closest('a')) return;
  
  this.style.transform = 'scale(0.98)';
  setTimeout(() => {
    this.style.transform = '';
  }, 200);
});
});

// Animate cards when they come into view
const observer = new IntersectionObserver((entries) => {
entries.forEach(entry => {
  if (entry.isIntersecting) {
    entry.target.style.opacity = '1';
    entry.target.style.transform = 'translateY(0)';
    observer.unobserve(entry.target);
  }
});
}, { threshold: 0.1 });

// Set initial state and observe
projectCards.forEach(card => {
card.style.opacity = '0';
card.style.transform = 'translateY(20px)';
card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
observer.observe(card);
});
});

//10:00
// Collaborators Filter and Interaction
document.addEventListener('DOMContentLoaded', function() {
// Filter functionality
const countryFilter = document.getElementById('country-filter');
const techFilter = document.getElementById('tech-filter');
const goalFilter = document.getElementById('goal-filter');
const collaborators = document.querySelectorAll('#collaborators-list .col');

function filterCollaborators() {
const countryValue = countryFilter.value;
const techValue = techFilter.value;
const goalValue = goalFilter.value;

collaborators.forEach(collaborator => {
  const countryMatch = countryValue === 'all' || collaborator.dataset.country === countryValue;
  const techMatch = techValue === 'all' || collaborator.dataset.tech === techValue;
  const goalMatch = goalValue === 'all' || collaborator.dataset.goal === goalValue;
  
  if (countryMatch && techMatch && goalMatch) {
    collaborator.style.display = 'block';
  } else {
    collaborator.style.display = 'none';
  }
});
}

// Add event listeners to filters
countryFilter.addEventListener('change', filterCollaborators);
techFilter.addEventListener('change', filterCollaborators);
goalFilter.addEventListener('change', filterCollaborators);

// Load more functionality
const loadMoreBtn = document.getElementById('load-more');
let visibleCount = 6; // Initial visible cards

// Hide cards beyond initial count
collaborators.forEach((collab, index) => {
if (index >= visibleCount) {
  collab.style.display = 'none';
}
});

loadMoreBtn.addEventListener('click', function() {
visibleCount += 3;

// Show next set of cards
collaborators.forEach((collab, index) => {
  if (index < visibleCount) {
    collab.style.display = 'block';
  }
});

// Hide button if all cards are visible
if (visibleCount >= collaborators.length) {
  loadMoreBtn.style.display = 'none';
}
});

// Connect button animation
document.querySelectorAll('.btn-outline-success').forEach(btn => {
btn.addEventListener('click', function(e) {
  e.preventDefault();
  const originalText = this.innerHTML;
  this.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Connecting...';
  
  setTimeout(() => {
    this.innerHTML = '<i class="bi bi-check-circle"></i> Connected';
    this.classList.remove('btn-outline-success');
    this.classList.add('btn-success');
  }, 1500);
});
});

// Initial filter to show India first (priority)
countryFilter.value = 'india';
filterCollaborators();
});

// 10:10
// Upcoming Events Data and Functionality
document.addEventListener('DOMContentLoaded', function() {
// Sample event data (in real implementation, this could come from an API)
const eventsData = {
hackathons: [
  {
    id: 1,
    title: "Climate Hack 2023",
    description: "48-hour hackathon focused on building solutions for carbon footprint reduction",
    date: "2023-11-15",
    location: "Virtual (Global)",
    tags: ["Climate Tech", "Open Source"],
    link: "#",
    organizer: "GreenTech Foundation"
  },
  {
    id: 2,
    title: "AI for Earth Challenge",
    description: "Build AI models to solve pressing environmental problems",
    date: "2023-12-05",
    location: "Bangalore, India",
    tags: ["AI/ML", "Sustainability"],
    link: "#",
    organizer: "EcoAI Collective"
  },
  {
    id: 3,
    title: "Urban Sustainability Hack",
    description: "Develop solutions for smart, sustainable cities",
    date: "2024-01-20",
    location: "Hybrid (Delhi & Online)",
    tags: ["Smart Cities", "IoT"],
    link: "#",
    organizer: "Urban Green Initiative"
  }
],
talks: [
  {
    id: 4,
    title: "The Future of Renewable Tech",
    description: "Panel discussion with industry leaders on emerging renewable technologies",
    date: "2023-11-22",
    location: "Online",
    tags: ["Renewable Energy", "Panel"],
    link: "#",
    organizer: "Clean Energy Forum"
  },
  {
    id: 5,
    title: "Blockchain for Carbon Markets",
    description: "How blockchain technology is transforming carbon credit systems",
    date: "2023-12-08",
    location: "Mumbai, India",
    tags: ["Blockchain", "Carbon Credits"],
    link: "#",
    organizer: "Digital Green"
  }
],
sprints: [
  {
    id: 6,
    title: "GSoC Prep Workshop",
    description: "Prepare for Google Summer of Code with open source climate projects",
    date: "2023-11-30",
    location: "Online",
    tags: ["GSoC", "Workshop"],
    link: "#",
    organizer: "Open Climate Collective"
  },
  {
    id: 7,
    title: "MLH Earth Day Hack",
    description: "Contribution sprint for environmental open source projects",
    date: "2024-04-22",
    location: "Global",
    tags: ["MLH", "Earth Day"],
    link: "#",
    organizer: "Major League Hacking"
  },
  {
    id: 8,
    title: "OpenAQ Contribution Day",
    description: "Help improve the open air quality data platform",
    date: "2023-12-12",
    location: "Virtual",
    tags: ["Open Source", "Data"],
    link: "#",
    organizer: "OpenAQ"
  }
]
};

// Function to create event cards
function createEventCard(event) {
const eventDate = new Date(event.date);
const monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

return `
  <div class="col">
    <div class="card event-card h-100">
      <div class="card-body">
        <div class="d-flex mb-3">
          <div class="event-date me-3">
            <div class="day">${eventDate.getDate()}</div>
            <div class="month">${monthNames[eventDate.getMonth()]}</div>
          </div>
          <div>
            <h5 class="card-title mb-1">${event.title}</h5>
            <p class="text-muted small mb-2">by ${event.organizer}</p>
            <div class="d-flex flex-wrap gap-2 mb-2">
              ${event.tags.map(tag => `<span class="event-tag">${tag}</span>`).join('')}
            </div>
          </div>
        </div>
        <p class="card-text">${event.description}</p>
        <div class="d-flex justify-content-between align-items-center mt-auto">
          <span class="text-muted small"><i class="bi bi-geo-alt"></i> ${event.location}</span>
          <a href="${event.link}" class="btn btn-sm btn-success">Register</a>
        </div>
      </div>
    </div>
  </div>
`;
}

// Function to load events into the DOM
function loadEvents() {
const hackathonsList = document.getElementById('hackathons-list');
const talksList = document.getElementById('talks-list');
const sprintsList = document.getElementById('sprints-list');

// Clear existing content
hackathonsList.innerHTML = '';
talksList.innerHTML = '';
sprintsList.innerHTML = '';

// Add hackathons
eventsData.hackathons.forEach(event => {
  hackathonsList.innerHTML += createEventCard(event);
});

// Add talks
eventsData.talks.forEach(event => {
  talksList.innerHTML += createEventCard(event);
});

// Add sprints
eventsData.sprints.forEach(event => {
  sprintsList.innerHTML += createEventCard(event);
});
}

// Initialize events
loadEvents();

// Calendar View Toggle
const toggleViewBtn = document.getElementById('toggle-view');
const listView = document.getElementById('eventsTabContent');
const calendarView = document.createElement('div');
calendarView.className = 'calendar-view';
calendarView.innerHTML = `
<div class="calendar-container mt-3">
  <div class="row g-0">
    <div class="col border calendar-day">
      <div class="calendar-day-header">Sun</div>
    </div>
    <div class="col border calendar-day">
      <div class="calendar-day-header">Mon</div>
    </div>
    <div class="col border calendar-day">
      <div class="calendar-day-header">Tue</div>
    </div>
    <div class="col border calendar-day">
      <div class="calendar-day-header">Wed</div>
    </div>
    <div class="col border calendar-day">
      <div class="calendar-day-header">Thu</div>
    </div>
    <div class="col border calendar-day">
      <div class="calendar-day-header">Fri</div>
    </div>
    <div class="col border calendar-day">
      <div class="calendar-day-header">Sat</div>
    </div>
  </div>
  <!-- Calendar rows would be generated here in a complete implementation -->
</div>
`;

listView.parentNode.insertBefore(calendarView, listView.nextSibling);

let isCalendarView = false;
toggleViewBtn.addEventListener('click', function() {
isCalendarView = !isCalendarView;

if (isCalendarView) {
  listView.style.display = 'none';
  calendarView.style.display = 'block';
  this.innerHTML = '<i class="bi bi-card-list"></i> Switch to List View';
} else {
  listView.style.display = 'block';
  calendarView.style.display = 'none';
  this.innerHTML = '<i class="bi bi-calendar-week"></i> Switch to Calendar View';
}
});

// In a complete implementation, you would:
// 1. Fetch events from an API instead of using sample data
// 2. Generate a proper calendar view with events placed on correct dates
// 3. Add pagination or "Load More" functionality for many events
// 4. Implement event search/filter functionality
});

//10:16
// Hall of Impact & Testimonials Functionality
document.addEventListener('DOMContentLoaded', function() {
// Sample leaderboard data
const leaderboardData = [
{
  rank: 1,
  name: "Sophia Chen",
  username: "@eco_sophia",
  avatar: "https://i.pravatar.cc/150?img=1",
  projects: ["FashionFootprint", "EcoSupplyChain"],
  badges: [
    { type: "opensource", label: "Open Source Warrior" },
    { type: "ai", label: "AI for Climate" }
  ],
  impact: "298 kg CO₂ reduced",
  joined: "Jan 2023"
},
{
  rank: 2,
  name: "Raj Patel",
  username: "@solar_raj",
  avatar: "https://i.pravatar.cc/150?img=5",
  projects: ["SolarForecast", "GreenGrid"],
  badges: [
    { type: "ai", label: "AI for Climate" },
    { type: "blockchain", label: "Blockchain for Green" }
  ],
  impact: "412 kg CO₂ reduced",
  joined: "Nov 2022"
},
{
  rank: 3,
  name: "Priya Sharma",
  username: "@blockchain_priya",
  avatar: "https://i.pravatar.cc/150?img=6",
  projects: ["CarbonChain", "EcoLedger"],
  badges: [
    { type: "blockchain", label: "Blockchain for Green" }
  ],
  impact: "385 kg CO₂ reduced",
  joined: "Mar 2023"
},
{
  rank: 4,
  name: "Aisha Patel",
  username: "@earthly_aisha",
  avatar: "https://i.pravatar.cc/150?img=2",
  projects: ["ForestGuard", "EcoVisual"],
  badges: [
    { type: "opensource", label: "Open Source Warrior" }
  ],
  impact: "267 kg CO₂ reduced",
  joined: "Feb 2023"
},
{
  rank: 5,
  name: "Carlos Mendez",
  username: "@wind_carlos",
  avatar: "https://i.pravatar.cc/150?img=9",
  projects: ["WindOpt", "TurbineAI"],
  badges: [
    { type: "ai", label: "AI for Climate" }
  ],
  impact: "245 kg CO₂ reduced",
  joined: "Apr 2023"
}
];

// Function to render leaderboard
function renderLeaderboard(data) {
const tbody = document.getElementById('leaderboard-body');
tbody.innerHTML = '';

data.forEach(user => {
  const row = document.createElement('tr');
  row.innerHTML = `
    <td>
      <div class="rank-badge ${user.rank <= 3 ? `rank-${user.rank}` : 'rank-other'}">
        ${user.rank}
      </div>
    </td>
    <td>
      <div class="d-flex align-items-center">
        <img src="${user.avatar}" alt="${user.name}" class="contributor-avatar">
        <div>
          <div class="fw-semibold">${user.name}</div>
          <div class="text-muted small">${user.username}</div>
        </div>
      </div>
    </td>
    <td>
      <div class="d-flex flex-wrap gap-1">
        ${user.projects.map(project => `<span class="badge bg-light text-dark">${project}</span>`).join('')}
      </div>
    </td>
    <td>
      <div class="d-flex flex-wrap gap-1">
        ${user.badges.map(badge => `
          <span class="badge ${`badge-${badge.type}`}">
            <span class="badge-icon">${badge.label.charAt(0)}</span>
            ${badge.label}
          </span>
        `).join('')}
      </div>
    </td>
    <td class="text-end fw-semibold text-success">
      ${user.impact}
    </td>
  `;
  tbody.appendChild(row);
});
}

// Initial render
renderLeaderboard(leaderboardData);

// Filter functionality
const timeFilter = document.getElementById('time-filter');
const badgeFilter = document.getElementById('badge-filter');

function applyFilters() {
const timeValue = timeFilter.value;
const badgeValue = badgeFilter.value;

let filteredData = [...leaderboardData];

// In a real implementation, you would fetch filtered data from the server
// This is just a client-side simulation
if (badgeValue !== 'all') {
  filteredData = filteredData.filter(user => 
    user.badges.some(badge => badge.type === badgeValue)
  );
}

renderLeaderboard(filteredData);
}

timeFilter.addEventListener('change', applyFilters);
badgeFilter.addEventListener('change', applyFilters);

// Testimonial carousel functionality
// (Would be implemented if you want rotating testimonials)
});
