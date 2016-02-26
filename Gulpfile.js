var gulp = require('gulp');
var browserify = require('browserify');
var reactify = require('reactify');
var uglify = require('gulp-uglify');
var buffer = require('vinyl-buffer');
var source = require('vinyl-source-stream');
var concat = require('gulp-concat');
var merge = require('merge-stream');

gulp.task('default', ['cameo', 'vendor', 'styles']);

gulp.task('cameo', function() {
   return browserify({
        entries: ['./js/cameo.js'],
        transform: [reactify],
        standalone: 'cameo'
   })
    .bundle()
    .pipe(source('cameo.js'))
    .pipe(buffer())
    .pipe(uglify())
    .pipe(gulp.dest('cameo/static/'));
});

gulp.task('styles', function() {
    return gulp.src([
        'node_modules/foundation-sites/dist/foundation.min.css',
        'node_modules/magnific-popup/dist/magnific-popup.css'
    ])
    .pipe(concat('styles.css'))
    .pipe(gulp.dest('cameo/static/'));
});

gulp.task('vendor', function() {
    return gulp.src([
        'node_modules/jquery/dist/jquery.min.js',
        'node_modules/magnific-popup/dist/jquery.magnific-popup.js'
    ])
    .pipe(concat('vendor.js'))
    .pipe(gulp.dest('cameo/static/'))
});