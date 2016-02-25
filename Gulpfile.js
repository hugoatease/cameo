var gulp = require('gulp');
var browserify = require('browserify');
var reactify = require('reactify');
var uglify = require('gulp-uglify');
var buffer = require('vinyl-buffer');
var source = require('vinyl-source-stream');

gulp.task('default', ['cameo', 'styles']);

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
   gulp.src('node_modules/foundation-sites/dist/foundation.min.css')
    .pipe(gulp.dest('cameo/static'));
});