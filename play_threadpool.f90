program concurrent
! Uses Fortran 2018 Coarray to work concurrently.
!
! It's not a process pool because the tasks are preset to specific workers.
! If some tasks finish earlier than others, some workers may sit idle with
! tasks still left to do.
!
! We use video playback to clearly demonstrate management of a fixed number of tasks
! until all tasks are done.
! I could have done this more simply, without an explicit coarray by
! co_broadcast(fwork,1) but this way is more general (in case fwork was very large N-D variable)
!
! usage:
! Give it a list of videos, most conveniently by globbing on the command line like:
!
! cafrun -np 3 pool ~/Videos/*.avi
!
! that will play 3 videos simultaneously, until all videos are complete

use, intrinsic:: iso_fortran_env, only: stderr=>error_unit
implicit none

integer, parameter :: N = 1024  ! arbitrarily longer than any file path we expect
integer :: argc, Nwork, i, ierr, istat, j, k
character(N) :: argv, errmsg
character(:), allocatable :: fname
character(N), allocatable, dimension(:), codimension[:] :: fwork
character(*), parameter :: cmd='ffplay -v warning -autoexit '

if(this_image() == 1) then
  argc = command_argument_count()
  if (argc==0) error stop 'must specify one or more files to play'

  Nwork = argc/num_images()
  if (modulo(argc,num_images()) /= 0) Nwork = Nwork + 1
endif

call co_broadcast(Nwork, 1)
allocate(fwork(Nwork)[*])

!> Assign tasks to workers (images)
if(this_image() == 1) then
  do i = 1,argc
    j = ceiling(i/real(num_images()))
    k = modulo(i,num_images()) + 1
    call get_command_argument(i, argv)
    ! print *, i,j,k
    fwork(j)[k] = argv
  enddo
endif

!> Ensure workers wait to be assigned their tasks
sync all

!> execute process pool with finite number of workers
do i = 1,Nwork
  fname = trim(fwork(i))
  if (len(fname) == N) exit  ! was not auto-allocated, due to unevenly divisible tasks/workers
  print '(I2,1X,A)', this_image(), fname

  call execute_command_line(cmd//fname, wait=.true., exitstat=istat, cmdstat=ierr, cmdmsg=errmsg)

  if (ierr /= 0) write(stderr,*) 'Return code', istat, errmsg, 'on image', this_image(), fname
enddo

end program
