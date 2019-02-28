program play_videos
! Uses Fortran 2018 co_broadcast to work concurrently
use, intrinsic:: iso_fortran_env, only: stderr=>error_unit
implicit none

integer, parameter :: N = 1024
character(N), allocatable :: flist(:)
integer :: argc, i, ierr, istat
character(N) :: argv, errmsg
character(:), allocatable :: fname
character(*), parameter :: cmd='ffplay -v warning -autoexit '

if(this_image() == 1) then
  argc = command_argument_count()
  if (argc==0) error stop 'must specify one or more files to play'
endif

call co_broadcast(argc, 1)
allocate(flist(argc))

if(this_image() == 1) then
  do i = 1,argc
    call get_command_argument(i, argv)
    flist(i) = argv
  enddo
endif

call co_broadcast(flist, 1)

do i = this_image(), argc, num_images()
  fname = trim(flist(i))
  print '(I2,1X,A)', this_image(), fname

  call execute_command_line(cmd//fname, wait=.true., &
    exitstat=istat, cmdstat=ierr, cmdmsg=errmsg)

  if (ierr /= 0) write(stderr,*) 'Return code', istat, errmsg, 'on image', this_image(), fname
enddo

end program
