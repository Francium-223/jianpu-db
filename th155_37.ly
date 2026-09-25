\version "2.20.0"
#(set-global-staff-size 20)

% un-comment the next line to remove Lilypond tagline:
% \header { tagline="" }

% comment out the next line if you're debugging jianpu-ly
% (but best leave it un-commented in production, since
% the point-and-click locations won't go to the user input)
\pointAndClickOff

\paper {
  print-all-headers = ##t %% allow per-score headers

  % un-comment the next line for A5:
  % #(set-default-paper-size "a5" )

  % un-comment the next line for no page numbers:
  % print-page-number = ##f

  % un-comment the next 3 lines for a binding edge:
  % two-sided = ##t
  % inner-margin = 20\mm
  % outer-margin = 10\mm

  % un-comment the next line for a more space-saving header layout:
  % scoreTitleMarkup = \markup { \center-column { \fill-line { \magnify #1.5 { \bold { \fromproperty #'header:dedication } } \magnify #1.5 { \bold { \fromproperty #'header:title } } \fromproperty #'header:composer } \fill-line { \fromproperty #'header:instrument \fromproperty #'header:subtitle \smaller{\fromproperty #'header:subsubtitle } } } }
}

%% 2-dot and 3-dot articulations
#(append! default-script-alist
   (list
    `(two-dots
       . (
           (script-priority . -200)
           (stencil . ,ly:text-interface::print)
           (text . ,#{ \markup \override #'(font-encoding . latin1) \center-align \bold ":" #})
           (padding . 0.20)
           (avoid-slur . inside)
           (side-axis . ,Y)
           (direction . ,UP)))))
#(append! default-script-alist
   (list
    `(three-dots
       . (
           (script-priority . -200)
           (stencil . ,ly:text-interface::print)
           (text . ,#{ \markup \override #'(font-encoding . latin1) \center-align \bold "⋮" #})
           (padding . 0.30)
           (avoid-slur . inside)
           (side-axis . ,Y)
           (direction . ,UP)))))
"two-dots" =
#(make-articulation 'two-dots)

"three-dots" =
#(make-articulation 'three-dots)

\layout {
  \context {
    \Score
    scriptDefinitions = #default-script-alist
  }
}

note-mod =
#(define-music-function
     (text note)
     (markup? ly:music?)
   #{
     \tweak NoteHead.stencil #ly:text-interface::print
     \tweak NoteHead.text
        \markup \lower #0.5 \sans \bold #text
     \tweak Rest.stencil #ly:text-interface::print
     \tweak Rest.text
        \markup \lower #0.5 \sans \bold #text
     #note
   #})

#(define (jianpu-glissando grob)
   (let* ((left-note (ly:spanner-bound grob LEFT))
          (right-note (ly:spanner-bound grob RIGHT))
          (left-y (ly:grob-property left-note 'Y-offset 0))
          (right-y (ly:grob-property right-note 'Y-offset 0))
          (left-event (ly:grob-property left-note 'cause))
          (right-event (ly:grob-property right-note 'cause))
          (left-pitch (and (ly:stream-event? left-event)
                           (ly:event-property left-event 'pitch)))
          (right-pitch (and (ly:stream-event? right-event)
                            (ly:event-property right-event 'pitch))))
     (if (and left-pitch right-pitch)
         (let* ((left-y-off (if (ly:pitch<? left-pitch right-pitch) (- left-y 0.9) (if (ly:pitch<? right-pitch left-pitch) (+ left-y 1.5) left-y)))
                (right-y-off (if (ly:pitch<? left-pitch right-pitch) (+ right-y 0.9) (if (ly:pitch<? right-pitch left-pitch) (- right-y 1.5) right-y)))
                (bd (ly:grob-property grob 'bound-details))
                (left-bd (list-copy (assoc-get 'left bd '())))
                (right-bd (list-copy (assoc-get 'right bd '())))
                (new-left-bd (assoc-set! left-bd 'Y left-y-off))
                (new-right-bd (assoc-set! right-bd 'Y right-y-off))
                (new-bd (list (cons 'left new-left-bd) (cons 'right new-right-bd))))
           (ly:grob-set-property! grob 'bound-details new-bd)))))
#(define (flip-beams grob)
   (ly:grob-set-property!
    grob 'stencil
    (ly:stencil-translate
     (let* ((stl (ly:grob-property grob 'stencil))
            (centered-stl (ly:stencil-aligned-to stl Y DOWN)))
       (ly:stencil-translate-axis
        (ly:stencil-scale centered-stl 1 -1)
        (* (- (car (ly:stencil-extent stl Y)) (car (ly:stencil-extent centered-stl Y))) 0) Y))
     (cons 0 -0.8))))

%=======================================================
#(define-event-class 'jianpu-grace-curve-event 'span-event)

#(define (add-grob-definition grob-name grob-entry)
   (set! all-grob-descriptions
         (cons ((@@ (lily) completize-grob-entry)
                (cons grob-name grob-entry))
               all-grob-descriptions)))

#(define (jianpu-grace-curve-stencil grob)
   (let* ((elts (ly:grob-object grob 'elements))
          (refp-X (ly:grob-common-refpoint-of-array grob elts X))
          (X-ext (ly:relative-group-extent elts refp-X X))
          (refp-Y (ly:grob-common-refpoint-of-array grob elts Y))
          (Y-ext (ly:relative-group-extent elts refp-Y Y))
          (direction (ly:grob-property grob 'direction RIGHT))
          (x-start (* 0.5 (+ (car X-ext) (cdr X-ext))))
          (y-start (+ (car Y-ext) 0.32))
          (x-start2 (if (eq? direction RIGHT)(+ x-start 0.5)(- x-start 0.5)))
          (x-end (if (eq? direction RIGHT)(+ (cdr X-ext) 0.2)(- (car X-ext) 0.2)))
          (y-end (- y-start 0.5))
          (stil (ly:make-stencil `(path 0.1
                                        (moveto ,x-start ,y-start
                                         curveto ,x-start ,y-end ,x-start ,y-end ,x-start2 ,y-end
                                         lineto ,x-end ,y-end))
                                  X-ext
                                  Y-ext))
          (offset (ly:grob-relative-coordinate grob refp-X X)))
     (ly:stencil-translate-axis stil (- offset) X)))

#(add-grob-definition
  'JianpuGraceCurve
  `(
     (stencil . ,jianpu-grace-curve-stencil)
     (meta . ((class . Spanner)
              (interfaces . ())))))

#(define jianpu-grace-curve-types
   '(
      (JianpuGraceCurveEvent
       . ((description . "Used to signal where curve encompassing music start and stop.")
          (types . (general-music jianpu-grace-curve-event span-event event))
          ))
      ))

#(set!
  jianpu-grace-curve-types
  (map (lambda (x)
         (set-object-property! (car x)
           'music-description
           (cdr (assq 'description (cdr x))))
         (let ((lst (cdr x)))
           (set! lst (assoc-set! lst 'name (car x)))
           (set! lst (assq-remove! lst 'description))
           (hashq-set! music-name-to-property-table (car x) lst)
           (cons (car x) lst)))
    jianpu-grace-curve-types))

#(set! music-descriptions
       (append jianpu-grace-curve-types music-descriptions))

#(set! music-descriptions
       (sort music-descriptions alist<?))


#(define (add-bound-item spanner item)
   (if (null? (ly:spanner-bound spanner LEFT))
       (ly:spanner-set-bound! spanner LEFT item)
       (ly:spanner-set-bound! spanner RIGHT item)))

jianpuGraceCurveEngraver =
#(lambda (context)
   (let ((span '())
         (finished '())
         (current-event '())
         (event-start '())
         (event-stop '()))
     `(
       (listeners
        (jianpu-grace-curve-event .
          ,(lambda (engraver event)
             (if (= START (ly:event-property event 'span-direction))
                 (set! event-start event)
                 (set! event-stop event)))))

       (acknowledgers
        (note-column-interface .
          ,(lambda (engraver grob source-engraver)
             (if (ly:spanner? span)
                 (begin
                  (ly:pointer-group-interface::add-grob span 'elements grob)
                  (add-bound-item span grob)))
             (if (ly:spanner? finished)
                 (begin
                  (ly:pointer-group-interface::add-grob finished 'elements grob)
                  (add-bound-item finished grob)))))
        (inline-accidental-interface .
          ,(lambda (engraver grob source-engraver)
             (if (ly:spanner? span)
                 (begin
                  (ly:pointer-group-interface::add-grob span 'elements grob)))
             (if (ly:spanner? finished)
                 (ly:pointer-group-interface::add-grob finished 'elements grob))))
        (script-interface .
          ,(lambda (engraver grob source-engraver)
             (let ((is-dyn (or (grob::has-interface grob 'dynamic-interface)
                       (eq? (ly:grob-property grob 'meta) 'DynamicText))))
               (if (and (ly:spanner? span) (not is-dyn))
                (ly:pointer-group-interface::add-grob span 'elements grob))
               (if (and (ly:spanner? finished) (not is-dyn))
                (ly:pointer-group-interface::add-grob finished 'elements grob))))))
       (process-music .
         ,(lambda (trans)
            (if (ly:stream-event? event-stop)
                (if (null? span)
                    (ly:warning "No start to this curve.")
                    (begin
                     (set! finished span)
                     (ly:engraver-announce-end-grob trans finished event-start)
                     (set! span '())
                     (set! event-stop '()))))
            (if (ly:stream-event? event-start)
                (begin
                 (set! span (ly:engraver-make-grob trans 'JianpuGraceCurve event-start))
                 (set! event-start '())))))
       
       (stop-translation-timestep .
         ,(lambda (trans)
            (if (and (ly:spanner? span)
                     (null? (ly:spanner-bound span LEFT)))
                (ly:spanner-set-bound! span LEFT
                  (ly:context-property context 'currentMusicalColumn)))
            (if (ly:spanner? finished)
                (begin
                 (if (null? (ly:spanner-bound finished RIGHT))
                     (ly:spanner-set-bound! finished RIGHT
                       (ly:context-property context 'currentMusicalColumn)))
                 (set! finished '())
                 (set! event-start '())
                 (set! event-stop '())))))
       
       (finalize
        (lambda (trans)
          (if (ly:spanner? finished)
              (begin
               (if (null? (ly:spanner-bound finished RIGHT))
                   (set! (ly:spanner-bound finished RIGHT)
                         (ly:context-property context 'currentMusicalColumn)))
               (set! finished '())))))
       )))

jianpuGraceCurveStart =
#(make-span-event 'JianpuGraceCurveEvent START)

jianpuGraceCurveEnd =
#(make-span-event 'JianpuGraceCurveEvent STOP)
%===========================================================

%{ The jianpu-ly input was:
%th155_37.txt
title=今宵は飄逸なエゴイスト(Live ver)　～ Egoistic Flowers.
tag=th155,东方凭依华,东方,touhou,东方原曲,ZUN,东方新作原曲,东方小数点作原曲
usertag=th155
tagroute=东方/东方原曲/ZUN/东方新作原曲/东方小数点作原曲/th155
MBID=ac3bf985-76fd-4d46-b60e-828943519eff
alias=今宵是飘逸的利己主义者(Live ver)　～ Egoistic Flowers.
status=ok
transcriber=Francium-223
todo=transcribe the crazy piano
%---
subtitle=intro
KeepLength
0c ,3 ,6 2 1c - ~ 1q 1 ,7 ,5 ,3c - ,3q 1 ,7 ,5
,3 ,#5 ,7 3 1c - ~ 1q 1 ,7 ,5 ,6c. 3q 3c 2q 3
5c 6 3 2q 3 ~ 3c - - - #5 - #5q 3 2 1
2 3 ，6c 3c. 2q ~ 2 3 ,6c 1. ,7. ,5
,3c ,#5 ,7 #5 6c - ~ 6q 3 6 7 '1 7 5c 6c. '1q ~ '1q 7 5 6 ~ 6c 5
6 - 5 - 6 - - -
%END
%}


\score {
<< \override Score.BarNumber.break-visibility = #center-visible
\override Score.BarNumber.Y-offset = -1
\set Score.barNumberVisibility = #(every-nth-bar-number-visible 5)

%% === BEGIN JIANPU STAFF ===
    \new RhythmicStaff \with {
    \consists "Accidental_engraver" 
    \consists \jianpuGraceCurveEngraver
    \omit Staff.DotColumn \omit Voice.Dots \override Glissando.before-line-breaking = #jianpu-glissando
    % Get rid of the stave but not the barlines:
    \override StaffSymbol.line-count = #0 % tested in 2.15.40, 2.16.2, 2.18.0, 2.18.2, 2.20.0 and 2.22.2
    \override BarLine.bar-extent = #'(-2 . 2) % LilyPond 2.18: please make barlines as high as the time signature even though we're on a RhythmicStaff (2.16 and 2.15 don't need this although its presence doesn't hurt; Issue 3685 seems to indicate they'll fix it post-2.18)
    $(add-grace-property 'Voice 'Stem 'direction DOWN)
    $(add-grace-property 'Voice 'Slur 'direction UP)
    $(add-grace-property 'Voice 'Stem 'length-fraction 0.5)
    $(add-grace-property 'Voice 'Beam 'beam-thickness 0.1)
    $(add-grace-property 'Voice 'Beam 'length-fraction 0.3)
    $(add-grace-property 'Voice 'Beam 'after-line-breaking flip-beams)
    $(add-grace-property 'Voice 'Beam 'Y-offset 2.5)
    $(add-grace-property 'Voice 'NoteHead 'Y-offset 2.5)
    }
    { \new Voice="W" {
    \override Beam.transparent = ##f
    \override Stem.direction = #DOWN
    \override Tie.staff-position = #2.5
    \tupletUp
    \tieUp
    \override Stem.length-fraction = #0
    \override Beam.beam-thickness = #0.1
    \override Beam.length-fraction = #0.5
    \override Beam.after-line-breaking = #flip-beams
    \override Voice.Rest.style = #'neomensural % this size tends to line up better (we'll override the appearance anyway)
    \override Accidental.font-size = #-4
    \override TupletBracket.bracket-visibility = ##t

    \override Staff.TimeSignature.style = #'numbered
    \override Staff.Stem.transparent = ##t
      \note-mod "0" r4  \note-mod "3" e4-\tweak #'Y-offset #-1.2 -\tweak #'X-offset #0.6 _. 
 \note-mod "6" a4-\tweak #'Y-offset #-1.2 -\tweak #'X-offset #0.6 _. 
 \note-mod "2" d'4 \once \override Tie.transparent = ##t \once \override Tie.staff-position = #0 | %{ bar 2: %}
 \note-mod "1" c'4
\=JianpuTie(  ~  \note-mod "–" c'4 \set stemLeftBeamCount = #0
\set stemRightBeamCount = #1
 \note-mod "1" c'8[
\=JianpuTie) \set stemLeftBeamCount = #1
\set stemRightBeamCount = #1
 \note-mod "1" c'8]
\set stemLeftBeamCount = #0
\set stemRightBeamCount = #1
 \note-mod "7" b8-\tweak #'X-offset #0.6 _. [
\set stemLeftBeamCount = #1
\set stemRightBeamCount = #1
 \note-mod "5" g8-\tweak #'X-offset #0.6 _. ]
\once \override Tie.transparent = ##t \once \override Tie.staff-position = #0 | %{ bar 3: %}
 \note-mod "3" e4-\tweak #'Y-offset #-1.2 -\tweak #'X-offset #0.6 _. 
 ~  \note-mod "–" e4 \set stemLeftBeamCount = #0
\set stemRightBeamCount = #1
 \note-mod "3" e8-\tweak #'X-offset #0.6 _. [
\set stemLeftBeamCount = #1
\set stemRightBeamCount = #1
 \note-mod "1" c'8]
\set stemLeftBeamCount = #0
\set stemRightBeamCount = #1
 \note-mod "7" b8-\tweak #'X-offset #0.6 _. [
\set stemLeftBeamCount = #1
\set stemRightBeamCount = #1
 \note-mod "5" g8-\tweak #'X-offset #0.6 _. ]
| %{ bar 4: %} \set stemLeftBeamCount = #0
\set stemRightBeamCount = #1
 \note-mod "3" e8-\tweak #'X-offset #0.6 _. [
\set stemLeftBeamCount = #1
\set stemRightBeamCount = #1
 \note-mod "5" \once \tweak Accidental.extra-offset #'(0 . 0.7)gis8-\tweak #'X-offset #0.6 _. ]
\set stemLeftBeamCount = #0
\set stemRightBeamCount = #1
 \note-mod "7" b8-\tweak #'X-offset #0.6 _. [
\set stemLeftBeamCount = #1
\set stemRightBeamCount = #1
 \note-mod "3" e'8]
\once \override Tie.transparent = ##t \once \override Tie.staff-position = #0  \note-mod "1" c'4
\=JianpuTie(  ~  \note-mod "–" c'4 | %{ bar 5: %} \set stemLeftBeamCount = #0
\set stemRightBeamCount = #1
 \note-mod "1" c'8[
\=JianpuTie) \set stemLeftBeamCount = #1
\set stemRightBeamCount = #1
 \note-mod "1" c'8]
\set stemLeftBeamCount = #0
\set stemRightBeamCount = #1
 \note-mod "7" b8-\tweak #'X-offset #0.6 _. [
\set stemLeftBeamCount = #1
\set stemRightBeamCount = #1
 \note-mod "5" g8-\tweak #'X-offset #0.6 _. ]
 \note-mod "6" a4.-\tweak #'Y-offset #-1.2 -\tweak #'X-offset #0.6 _. 
\set stemLeftBeamCount = #0
\set stemRightBeamCount = #1
 \note-mod "3" e'8[]
| %{ bar 6: %}
 \note-mod "3" e'4
\set stemLeftBeamCount = #0
\set stemRightBeamCount = #1
 \note-mod "2" d'8[
\set stemLeftBeamCount = #1
\set stemRightBeamCount = #1
 \note-mod "3" e'8]
 \note-mod "5" g'4  \note-mod "6" a'4 | %{ bar 7: %}
 \note-mod "3" e'4
\set stemLeftBeamCount = #0
\set stemRightBeamCount = #1
 \note-mod "2" d'8[
\set stemLeftBeamCount = #1
\set stemRightBeamCount = #1
 \note-mod "3" e'8]
~ \once \override Tie.transparent = ##t \once \override Tie.staff-position = #0  \note-mod "3" e'4
\=JianpuTie(  ~ \once \override Tie.transparent = ##t \once \override Tie.staff-position = #0  \note-mod "–" e'4
 ~ \once \override Tie.transparent = ##t \once \override Tie.staff-position = #0 | %{ bar 8: %}
 \note-mod "3" e'4 \=JianpuTie)
 ~  \note-mod "–" e'4 \once \override Tie.transparent = ##t \once \override Tie.staff-position = #0  \note-mod "5" \once \tweak Accidental.extra-offset #'(0 . 0.7)gis'4
 ~  \note-mod "–" gis'4 | %{ bar 9: %} \set stemLeftBeamCount = #1
\set stemRightBeamCount = #1
 \note-mod "5" \once \tweak Accidental.extra-offset #'(0 . 0.7)gis'8[
\set stemLeftBeamCount = #1
\set stemRightBeamCount = #1
 \note-mod "3" e'8]
\set stemLeftBeamCount = #0
\set stemRightBeamCount = #1
 \note-mod "2" d'8[
\set stemLeftBeamCount = #1
\set stemRightBeamCount = #1
 \note-mod "1" c'8]
\set stemLeftBeamCount = #0
\set stemRightBeamCount = #1
 \note-mod "2" d'8[
\set stemLeftBeamCount = #1
\set stemRightBeamCount = #1
 \note-mod "3" e'8]
 \note-mod "6" a4-\tweak #'Y-offset #-1.2 -\tweak #'X-offset #0.6 _. 
| %{ bar 10: %}
 \note-mod "3" e'4.
\set stemLeftBeamCount = #0
\set stemRightBeamCount = #1
 \note-mod "2" d'8[]
~ \set stemLeftBeamCount = #0
\set stemRightBeamCount = #1
 \note-mod "2" d'8[
\set stemLeftBeamCount = #1
\set stemRightBeamCount = #1
 \note-mod "3" e'8]
 \note-mod "6" a4-\tweak #'Y-offset #-1.2 -\tweak #'X-offset #0.6 _. 
| %{ bar 11: %}
 \note-mod "1" c'4.
 \note-mod "7" b4.-\tweak #'Y-offset #-1.2 -\tweak #'X-offset #0.6 _. 
 \note-mod "5" g4-\tweak #'Y-offset #-1.2 -\tweak #'X-offset #0.6 _. 
| %{ bar 12: %}
 \note-mod "3" e4-\tweak #'Y-offset #-1.2 -\tweak #'X-offset #0.6 _. 
 \note-mod "5" \once \tweak Accidental.extra-offset #'(0 . 0.7)gis4-\tweak #'Y-offset #-1.2 -\tweak #'X-offset #0.6 _. 
 \note-mod "7" b4-\tweak #'Y-offset #-1.2 -\tweak #'X-offset #0.6 _. 
 \note-mod "5" \once \tweak Accidental.extra-offset #'(0 . 0.7)gis'4
\once \override Tie.transparent = ##t \once \override Tie.staff-position = #0 | %{ bar 13: %}
 \note-mod "6" a'4
\=JianpuTie(  ~  \note-mod "–" a'4 \set stemLeftBeamCount = #0
\set stemRightBeamCount = #1
 \note-mod "6" a'8[
\=JianpuTie) \set stemLeftBeamCount = #1
\set stemRightBeamCount = #1
 \note-mod "3" e'8]
\set stemLeftBeamCount = #0
\set stemRightBeamCount = #1
 \note-mod "6" a'8[
\set stemLeftBeamCount = #1
\set stemRightBeamCount = #1
 \note-mod "7" b'8]
| %{ bar 14: %} \set stemLeftBeamCount = #0
\set stemRightBeamCount = #1
 \note-mod "1" c''8^.[
\set stemLeftBeamCount = #1
\set stemRightBeamCount = #1
 \note-mod "7" b'8]
 \note-mod "5" g'4  \note-mod "6" a'4. \set stemLeftBeamCount = #0
\set stemRightBeamCount = #1
 \note-mod "1" c''8^.[]
~ | %{ bar 15: %} \set stemLeftBeamCount = #0
\set stemRightBeamCount = #1
 \note-mod "1" c''8^.[
\set stemLeftBeamCount = #1
\set stemRightBeamCount = #1
 \note-mod "7" b'8]
\set stemLeftBeamCount = #0
\set stemRightBeamCount = #1
 \note-mod "5" g'8[
\set stemLeftBeamCount = #1
\set stemRightBeamCount = #1
 \note-mod "6" a'8]
~  \note-mod "6" a'4  \note-mod "5" g'4 \once \override Tie.transparent = ##t \once \override Tie.staff-position = #0 | %{ bar 16: %}
 \note-mod "6" a'4
 ~  \note-mod "–" a'4 \once \override Tie.transparent = ##t \once \override Tie.staff-position = #0  \note-mod "5" g'4
 ~  \note-mod "–" g'4 \once \override Tie.transparent = ##t \once \override Tie.staff-position = #0 | %{ bar 17: %}
 \note-mod "6" a'4
 ~ \once \override Tie.transparent = ##t \once \override Tie.staff-position = #0  \note-mod "–" a'4
 ~ \once \override Tie.transparent = ##t \once \override Tie.staff-position = #0  \note-mod "–" a'4
 ~  \note-mod "–" a'4 \bar "|." } }
% === END JIANPU STAFF ===

>>
\header{
title="今宵は飄逸なエゴイスト(Live ver)　~ Egoistic Flowers."
tag="th155,东方凭依华,东方,touhou,东方原曲,ZUN,东方新作原曲,东方小数点作原曲"
usertag="th155"
tagroute="东方/东方原曲/ZUN/东方新作原曲/东方小数点作原曲/th155"
mbid="ac3bf985-76fd-4d46-b60e-828943519eff"
alias="今宵是飘逸的利己主义者(Live ver)　~ Egoistic Flowers."
status="ok"
transcriber="Francium-223"
todo="transcribe the crazy piano"
subtitle="intro"
}
\layout{
  \context {
    \Global
    \grobdescriptions #all-grob-descriptions
  }
} }
\score {
\unfoldRepeats
<< 

% === BEGIN MIDI STAFF ===
    \new Staff { \new Voice="X" { r4 e4 a4 d'4 | %{ bar 2: %} c'2 ~ c'8 c'8 b8 g8 | %{ bar 3: %} e2 e8 c'8 b8 g8 | %{ bar 4: %} e8 gis8 b8 e'8 c'2 ~ | %{ bar 5: %} c'8 c'8 b8 g8 a4. e'8 | %{ bar 6: %} e'4 d'8 e'8 g'4 a'4 | %{ bar 7: %} e'4 d'8 e'8 ~ e'2  ~ | %{ bar 8: %} e'2 gis'2 | %{ bar 9: %} gis'8 e'8 d'8 c'8 d'8 e'8 a4 | %{ bar 10: %} e'4. d'8 ~ d'8 e'8 a4 | %{ bar 11: %} c'4. b4. g4 | %{ bar 12: %} e4 gis4 b4 gis'4 | %{ bar 13: %} a'2 ~ a'8 e'8 a'8 b'8 | %{ bar 14: %} c''8 b'8 g'4 a'4. c''8 ~ | %{ bar 15: %} c''8 b'8 g'8 a'8 ~ a'4 g'4 | %{ bar 16: %} a'2 g'2 | %{ bar 17: %} a'1 } }
% === END MIDI STAFF ===

>>
\header{
title="今宵は飄逸なエゴイスト(Live ver)　~ Egoistic Flowers."
tag="th155,东方凭依华,东方,touhou,东方原曲,ZUN,东方新作原曲,东方小数点作原曲"
usertag="th155"
tagroute="东方/东方原曲/ZUN/东方新作原曲/东方小数点作原曲/th155"
mbid="ac3bf985-76fd-4d46-b60e-828943519eff"
alias="今宵是飘逸的利己主义者(Live ver)　~ Egoistic Flowers."
status="ok"
transcriber="Francium-223"
todo="transcribe the crazy piano"
subtitle="intro"
}
\midi { \context { \Score tempoWholesPerMinute = #(ly:make-moment 84 4)}} }
