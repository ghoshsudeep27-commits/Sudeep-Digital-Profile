/* ==========================================================================
   gallery.js — shared gallery builder + lightbox
   Loaded by every page. One copy, so a fix lands everywhere at once.

   What it does
   ------------
   1. Builds the carousels that exist on the current page from CONFIG below.
      Only tracks present in the DOM are built, so one file serves all pages.
   2. Adds real alt text per image, keyed by the number in the filename.
   3. Provides window.initLightbox(), which binds every [data-full] element.
   4. Dispatches 'galleriesReady' once the slides exist, which is what each
      page's carousel script listens for.

   Adding a photo: drop train_23.jpg into images/ and set 'train-track' to 23
   in COUNTS. Adding a testimonial image: nothing to do here, the testimonial
   cards link straight to images/testi_NN.jpg through data-full.
   ========================================================================== */
(function () {
  'use strict';

  var CONFIG = {
    'train-track': {
      prefix: 'train_',
      altPrefix: 'Training photo',
      cardClass: 'gallery-item',
      overlaySvg: '<div class="gallery-item__overlay"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg></div>',
      alts: {
      1: "Sudeep Ghosh presenting the Respectful Patient Interaction and Emotional Care module to a room of students, with the slide on screen.",
      2: "Sudeep Ghosh leading a session in a corporate classroom, standing beside a wall-mounted screen with participants at desks.",
      3: "Sudeep Ghosh at the front of a classroom, presenting to participants taking notes along a long table.",
      4: "Hospital training session with nurses in scrubs and face masks seated in rows while Sudeep Ghosh speaks.",
      5: "Healthcare session in a hospital seminar room, with nurses in caps and a slide projected at the front.",
      6: "Sudeep Ghosh receiving a bouquet in front of a printed banner at a college event.",
      7: "Group photograph of students in white shirts and ties with Sudeep Ghosh, seated in a hall.",
      8: "Group photograph of students and staff outside a college building after a training session.",
      9: "Group photograph of participants outside Government Polytechnic Lisana, including several people in wheelchairs.",
      10: "Group photograph of students in blazers with staff, seated and standing under a college portico.",
      11: "Sudeep Ghosh speaking at a lectern in front of the Baba Mastnath University Employability Enhancement Training Programme banner.",
      12: "Sudeep Ghosh presenting at a screen in a computer lab, with students seated at the benches.",
      13: "Nurses in scrubs, caps and face masks seated with notebooks in a hospital training room.",
      14: "Sudeep Ghosh receiving a memento from a school principal and staff in a classroom.",
      15: "Sudeep Ghosh addressing hospital staff, some in scrubs and masks, seated in rows in a training room.",
      16: "Sudeep Ghosh addressing a room of nurses and hospital staff in scrubs, caps and masks, several taking notes.",
      17: "Sudeep Ghosh presenting to nursing staff in a hospital training room, with a laptop and projector on the desk beside him.",
      18: "Sudeep Ghosh speaking to a room of nurses in scrubs and caps, with staff in the front row holding notebooks.",
      19: "Slightly blurred photograph of Sudeep Ghosh during a classroom session, with students standing at the back of the room.",
      20: "Seven participants holding their certificates behind Sudeep Ghosh, who is seated at the front of the classroom.",
      21: "Slightly blurred photograph of Sudeep Ghosh talking with hospital staff in a ward corridor, with charts on the wall behind.",
      22: "Sudeep Ghosh presenting a slide titled Empathy: The Foundation of Patient Trust at a dental clinic, with framed certificates on the wall behind."
      },
    },
    'press-track': {
      prefix: 'press_',
      altPrefix: 'Press clipping',
      cardClass: 'press-item',
      overlaySvg: '',
      alts: {
      1: "Pal Pal News clipping, Rohtak: Employability enhancement training begins at Baba Mastnath University, with a photograph of Sudeep Ghosh addressing students.",
      2: "Punjabi press clipping: Employment training workshop at Guru Hargobind Sahib Khalsa Girls College, Balbera, run with Mahindra and Mahindra for 70 students.",
      3: "Desh Pardesh Times clipping: Six-day employment training workshop at Guru Hargobind Sahib Khalsa Girls College, Balbera, with photographs of the speakers and the student audience.",
      4: "Desh Pardesh Times clipping: Placement training camp at Karhali Sahib College, with a photograph of Sudeep Ghosh teaching a classroom of students.",
      5: "Desh Pardesh Times clipping: Two-day placement training camp concludes at Karhali Sahib College, with students seated in a classroom session.",
      6: "Punjabi press clipping, Amritsar: Mock interview session for final-semester students at Sri Guru Hargobind Sahib Khalsa Girls College, with the principal and students photographed together.",
      7: "Sach Di Pehchan clipping, Batala: Two-day workshop by the placement cell of Guru Nanak College begins, shown in four photographs including the lamp-lighting ceremony and classroom sessions.",
      8: "Punjabi press clipping, Batala: Two-day placement workshop at Guru Nanak College, with a photograph of the principal and staff presenting a bouquet.",
      9: "Hindi press clipping, Safidon: Workshop teaching interview skills to students at Government PG College, Safidon, with a group photograph of participants.",
      10: "Hindi press clipping, Safidon: Body language workshop at Government PG College, Safidon, with a photograph of Sudeep Ghosh addressing students.",
      11: "Hindi press clipping, Safidon: Six-day personality development and interview skills training at Government College, Safidon, with Sudeep Ghosh teaching a full classroom.",
      12: "Savera News clipping, Garhshankar: Seven-day employability and skills training programme begins at Akali Memorial Khalsa College, with staff photographed at the launch.",
      13: "Hindi press clipping, Jind: Employability skills workshop running to 4 September at Hindu Kanya Mahavidyalaya, Jind, with a photograph of a session in the computer lab.",
      14: "Hindi press clipping, Jind: Employability skills training at Hindu Kanya Mahavidyalaya, with Sudeep Ghosh addressing students in the computer lab.",
      15: "Hindi press clipping, Safidon: Week-long workshop on critical thinking and problem solving concludes at Government PG College, Safidon.",
      16: "Hindi press clipping, Rohtak: Seven-day workshop with the Department of Sociology, Maharshi Dayanand University and Naandi Foundation, with a group photograph outside the department.",
      17: "Hindi press clipping, Safidon: Six-day personality development and interview skills training begins at Government College, Safidon, with a photograph of the classroom.",
      18: "Hindi press clipping, Safidon: Week-long workshop concludes at Government PG College, Safidon, with a group photograph of students and the trainer.",
      19: "Ajit clipping, Garhshankar: Employability and skills training programme concludes at Akali Memorial Khalsa College, with Sudeep Ghosh being honoured on stage.",
      20: "Dainik Savera clipping, Tohana: Week-long personality development and corporate culture training begins at Mata Gujri College, Fatehabad, with a photograph of the session.",
      21: "Desh Pardesh Times clipping: Placement training camp at Karhali Sahib College, with Sudeep Ghosh teaching a classroom of students.",
      22: "Punjabi press clipping, Bathinda: Seven-day employability skills workshop at SSD Girls College, 24 to 30 July 2024, with photographs of the sessions and participants.",
      23: "Dainik Bhaskar news brief, Rohtak: Employability Skills Enhancement workshop at Maharshi Dayanand University, 19 November 2025, with students in the audience.",
      24: "Punjab Kesri clipping, Rohtak: Employability Skills Enhancement workshop at Maharshi Dayanand University, with Sudeep Ghosh addressing students."
      },
    }
  };

  // Known image counts — the list is built directly instead of probing 1..99,
  // which downloaded every image on page load just to detect which existed.
  var COUNTS = { 'train-track': 22, 'press-track': 24 };

  function pad(n) { return n < 10 ? '0' + n : '' + n; }

  // Alt text is keyed by the number in the filename, not by position: the array
  // is reversed so the newest image shows first, so a positional lookup would
  // pair every alt with the wrong picture.
  function altFor(config, src) {
    var n = parseInt(String(src).replace(/[^0-9]/g, ''), 10);
    return (config.alts && config.alts[n]) || (config.altPrefix + ' ' + n);
  }

  function buildGallery(trackId, config) {
    var track = document.getElementById(trackId);
    if (!track) return;
    var count = COUNTS[trackId] || 0;
    var images = [];
    for (var i = 1; i <= count; i++) {
      images.push('images/' + config.prefix + pad(i) + '.jpg');
    }
    images.reverse(); // newest (highest-numbered) first
    images.forEach(function (src, idx) {
      var slide = document.createElement('div');
      slide.className = 'carousel__slide';
      slide.innerHTML = '<div class="' + config.cardClass + ' reveal" style="--i:' + idx + '" data-full="' + src + '">'
        + '<img src="' + src + '" alt="' + altFor(config, src) + '" loading="lazy">'
        + config.overlaySvg
        + '</div>';
      track.appendChild(slide);
    });
  }

  /* ---- Lightbox: defined immediately, so inline scripts can call it ---- */
  window.initLightbox = function () {
    var lb = document.getElementById('lightbox');
    var lbImg = document.getElementById('lbImg');
    var lbClose = document.getElementById('lbClose');
    if (!lb) return;
    document.querySelectorAll('[data-full]').forEach(function (el) {
      if (el.dataset.lightboxBound) return;
      el.dataset.lightboxBound = '1';
      el.addEventListener('click', function () {
        var thumb = el.querySelector('img');
        lbImg.alt = thumb && thumb.alt ? thumb.alt : (el.getAttribute('aria-label') || 'Full size view');
        lbImg.src = el.dataset.full;
        lb.classList.add('open');
        document.body.style.overflow = 'hidden';
      });
    });
    if (lb.dataset.bound) return;
    lb.dataset.bound = '1';
    var close = function () {
      lb.classList.remove('open');
      lbImg.src = '';
      document.body.style.overflow = '';
    };
    lb.addEventListener('click', function (e) { if (e.target === lb || e.target === lbClose) close(); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') close(); });
  };
  window.initLightbox();

  /* ---- Build on DOMContentLoaded, not before -------------------------
     The pages register their 'galleriesReady' listener (which starts the
     carousels) further down the same script. Firing earlier would leave the
     carousels built but never initialised. */
  function start() {
    var jobs = [];
    Object.keys(CONFIG).forEach(function (id) {
      if (document.getElementById(id)) jobs.push(buildGallery(id, CONFIG[id]));
    });
    if (!jobs.length) return;
    Promise.all(jobs).then(function () {
      window.dispatchEvent(new Event('galleriesReady'));
      window.initLightbox();
    });
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', start);
  } else {
    start();
  }
})();
