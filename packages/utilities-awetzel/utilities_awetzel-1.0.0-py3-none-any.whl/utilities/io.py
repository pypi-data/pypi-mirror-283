'''
Utility functions for reading, writing, printing.

@author: Andrew Wetzel <arwetzel@gmail.com>
'''

import os
import glob
import time
import datetime
import numpy as np
import h5py


# --------------------------------------------------------------------------------------------------
# useful classes
# --------------------------------------------------------------------------------------------------
class DictClass(dict):
    '''
    Use to generate dictionary class for more flexibility.
    '''


# --------------------------------------------------------------------------------------------------
# print at run-time
# --------------------------------------------------------------------------------------------------
class ListPropClass:
    '''
    Print self and attributes in nice format.

    Use by importing this class into another class.
    '''

    def __repr__(self):
        return '< Instance of {}:\n{}>'.format(
            self.__module__ + '.' + self.__class__.__name__, self.get_attr_names()
        )

    def get_attr_names(self):
        '''
        .
        '''
        result = ''
        for attr in self.__dict__:
            if attr[:2] == '__':
                result += f'  self.{attr} = <built-in>\n'
            else:
                result += f'  self.{attr} = {self.__dict__[attr]}\n'

        return result


class ManualProgressBar:
    '''
    Create a progress bar.
    Simple, but should work in all cases.

    Usage:
        progress_bar = ManualProgressBar(ar.size, 'looping')
        progress_bar.start()
        for ii, item in enumerate(ar):
            # do stuff
            progress_bar.update(ii)
        progress_bar.finish()
    '''

    def __init__(self, maxi, label=None, max_width=70, character='='):
        '''
        .
        '''
        self.label = label if label is not None else ''
        self.maxi = maxi
        self.bar_length = max_width - len(self.label)
        self.character = character
        self.end_string = '] ({:04.1f}%)'

    def start(self):
        '''
        .
        '''
        print(self.label + ' [', end='')
        print((' ' * self.bar_length) + self.end_string.format(0), end='', flush=True)

    def reset(self):
        '''
        .
        '''
        print('\b' * (self.bar_length + len(self.end_string.format(0))), end='', flush=True)

    def update(self, ii):
        '''
        .
        '''
        frac_done = ii * 1.0 / self.maxi
        filled = int(np.rint(frac_done * self.bar_length)) * self.character
        empty = ' ' * int((self.bar_length - len(filled)))
        self.reset()
        print(filled + empty + self.end_string.format(frac_done * 100), end='', flush=True)

    def finish(self):
        '''
        .
        '''
        self.update(self.maxi)
        print(flush=True)


class SayClass(ListPropClass):
    '''
    Print comments and diagnostics at run time in nice format.

    Use by importing this class into antother class or declaring within a function.
    '''

    print_function_name = True

    def __init__(self, func=None):
        '''
        Parameters
        ----------
        func : func
            function (to get its name for printing), if not using SayClass within a class
        '''
        if func is not None:
            self.func_name = func.__module__ + '.' + func.__name__
        elif 'SayClass' in str(self.__class__):
            raise ValueError('need to pass function to get name')

    def say(self, string, verbose=True, end='\n'):
        '''
        Print string in nice format.

        Parameters
        ----------
        string : str
            string to print
        verbose : bool
            whether to print
        end : str
            end of string to pass to print()
        '''
        if not verbose:
            return

        if string:
            if string[0] != '!' and string[0] != '*' and string[0] != '#':
                string = '  ' + string

            if self.print_function_name:
                print()
                if 'SayClass' in str(self.__class__):
                    print(f'# in {self.func_name}():')
                else:
                    print(
                        '# in {}():'.format(
                            self.__module__ + '.' + self.__class__.__name__.replace('Class', '')
                        )
                    )

                self.print_function_name = False

        print(string, end=end)

        os.sys.stdout.flush()

    def make_progress_bar(self, max_iter, label=None):
        '''
        Return a progressbar instance, either via ProgressBar or manually.
        '''
        try:
            from progressbar import ProgressBar, Bar, Percentage, ETA

            if label is not None:
                widgets = [
                    '{0} ('.format(label),
                    Percentage(),
                    ') ',
                    Bar(left='[', right=']', marker='-'),
                    ' ',
                    ETA(),
                ]
            else:
                widgets = [
                    '(',
                    Percentage(),
                    ') ',
                    Bar(left='[', right=']', marker='-'),
                    ' ',
                    ETA(),
                ]
            return ProgressBar(widgets=widgets, maxval=max_iter)

        except ImportError:
            return ManualProgressBar(max_iter, label)


class WriteClass:
    '''
    Class to store behavior for printing - either print to stdout or write to file or both.
    '''

    def __init__(self, file_out=None, print_stdout=False):
        '''
        Parameters
        ----------
        file_out : file object
            output file to write to
        print_stdout : bool
            whether to print to stout in addition to writing to file
        '''
        self.file_out = file_out
        self.print_stdout = print_stdout

    def write(self, string, print_stdout=None):
        '''
        Print string to stdout or to file, depending on whether self.file_out is defined.

        Parameters
        ----------
        string : str
            string to write
        print_stdout : bool
            whether to print to stout in addition to writing to file
        '''
        if self.file_out:
            self.file_out.write(string + '\n')
            if print_stdout is None:
                if self.print_stdout:
                    print(string)
            elif print_stdout:
                print(string)
        else:
            print(string)


def print_flush(string, end='\n'):
    '''
    Print and instantly flush std output.

    Parameters
    ----------
    string : str
    end : str
    '''
    print(string, end=end)

    os.sys.stdout.flush()


def get_string_from_numbers(values, digits=3, exponential=None, strip=False):
    '''
    Get string of number[s] in nice format.

    Parameters
    ----------
    value[s] : int/float or list
        numbers to get string for
    digits : int
        number of digits after period
    exponential : bool
        whether to use exponential (instead of float) notation. if None, choose automatically
    strip : bool
        whether to strip trailing 0s (and .)

    Returns
    -------
    string : str
    '''
    if not np.isscalar(values):
        # multiple values, need to parse
        strings = ''
        for value in values:
            strings += get_string_from_numbers(value, digits) + ', '
        return strings[:-2]

    # single value
    value = values

    if not np.isfinite(value):
        string = '{}'
    elif isinstance(value, int) or (isinstance(value, np.ndarray) and 'int' in str(value.dtype)):
        string = '{:d}'
    elif exponential is False:
        # use float format
        string = f'{{:.{digits}f}}'
    elif exponential or np.abs(value) >= 1e5 or 0 < np.abs(value) <= 1e-4:
        # use exponential format
        exponential = True
        string = f'{{:.{digits}e}}'
    else:
        string = f'{{:.{digits}f}}'

    if exponential:
        string = string.format(value)
        string = string.replace('+', '')
        string = string.replace('e0', 'e')
        string = string.replace('e-0', 'e-')

        if strip:
            strings = string.split('e')
            strings[0] = strings[0].rstrip('0').rstrip('.')
            string = strings[0] + 'e' + strings[1]

    else:
        string = string.format(values)

        if strip and string != '0':
            string = string.rstrip('0').rstrip('.')

    return string


def print_array(values, form='{:.3f}', delimeter=', ', end='\n'):
    '''
    Print values of array in nice format.

    Parameters
    ----------
    values : array-like
    form : str
        format to print
    delimeter : str
        delimeter to print between numbers
    end : str
        ending of string to pass to print()
    '''
    if np.isscalar(values):
        string = form
    else:
        string = form + delimeter

    for value in values[:-1]:
        print(string.format(value), end='')
    print(form.format(values[-1]), end=end)


# --------------------------------------------------------------------------------------------------
# print within batch script
# --------------------------------------------------------------------------------------------------
class SubmissionScriptClass:
    '''
    Helper functions and run-time information for batch submission script.
    '''

    def __init__(self, scheduler_name='slurm', node_number=None, mpi_number_per_node=None):
        '''
        Get type of batch scheduler.
        Print pre-run information on job settings.
        Only need to import parameters if using PBS scheduler.

        Parameters
        ----------
        scheduler_name : str
            'slurm' or 'pbs'
        node_number : int
            number of nodes
        mpi_number_per_node : int
            number of MPI tasks per node
        '''
        assert scheduler_name in ['slurm', 'pbs']

        self.scheduler_name = scheduler_name

        os.system('date')
        print('')

        if 'slurm' in self.scheduler_name:
            self.node_number = int(os.environ['SLURM_JOB_NUM_NODES'])
            self.mpi_number = int(os.environ['SLURM_NTASKS'])
            self.mpi_number_per_node = self.mpi_number // self.node_number

            if 'SLURM_CPUS_PER_TASK' in os.environ:
                # copy to value to OMP_NUM_THREADS to enable OpenMP in Gizmo
                os.environ['OMP_NUM_THREADS'] = os.environ['SLURM_CPUS_PER_TASK']
                self.omp_number = int(os.environ['SLURM_CPUS_PER_TASK'])
                if self.omp_number < 1:
                    self.omp_number = 1
            else:
                self.omp_number = 1

            print('job name = {}'.format(os.environ['SLURM_JOB_NAME']))
            print('job id = {}\n'.format(os.environ['SLURM_JOB_ID']))
            print('using the following resources:')
            print('  {} nodes'.format(os.environ['SLURM_JOB_NUM_NODES']))
            print(
                '  {} MPI tasks per node, {} MPI tasks total'.format(
                    os.environ['SLURM_TASKS_PER_NODE'], os.environ['SLURM_NTASKS']
                )
            )
            if self.omp_number > 1:
                print('  {} OpenMP threads per MPI task'.format(os.environ['OMP_NUM_THREADS']))

        elif 'pbs' in self.scheduler_name:
            assert node_number and mpi_number_per_node
            self.node_number = node_number
            self.mpi_number_per_node = mpi_number_per_node
            self.mpi_number = self.mpi_number_per_node * self.node_number
            self.omp_number = int(os.environ['OMP_NUM_THREADS'])

            print('job name = {}'.format(os.environ['PBS_JOBNAME']))
            print('job id = {}\n'.format(os.environ['PBS_JOBID']))
            print('using the following resources:')
            print(f'  {self.node_number} nodes')
            print(
                f'  {self.mpi_number_per_node} MPI tasks per node,'
                + f' {self.mpi_number} MPI tasks total'
            )
            if self.omp_number >= 1:
                print(f'  {self.omp_number} OpenMP threads per MPI task')
                if self.omp_number < 1:
                    self.omp_number = 1
            else:
                self.omp_number = 1  # ensure 1 for sanity

        self.core_number = self.mpi_number * self.omp_number
        print(f'  {self.core_number} cores\n')
        os.sys.stdout.flush()

        self.time_ini = time.time()

    def print_runtime(self):
        '''
        Print run time information of job.
        '''
        time_dif = time.time() - self.time_ini
        time_dif_str = str(datetime.timedelta(seconds=time_dif))

        print('')
        print(
            'wall time: {:.0f} sec = {:.2f} day = {}'.format(
                time_dif, time_dif / 3600 / 24, time_dif_str.split('.', maxsplit=1)[0]
            )
        )
        print('core-hours: {:.1f}'.format(time_dif * self.core_number / 3600))
        print('node-hours: {:.1f}\n'.format(time_dif * self.node_number / 3600))

        os.sys.stdout.flush()

        os.system('date')

    def check_existing_job(self, file_name, submit_before=False, time_delay=4):
        '''
        Check if defined/input jobid that needs to finish before this starts.

        Parameters
        ----------
        file_name : str
            name of submission script file
        submit_before : bool
            whether to submit a follow-up job before this one starts (to wait in queue)
        time_delay : float
            how long [hr] to wait if follow-up tries to start before current finishes
        '''
        import subprocess

        if 'slurm' in self.scheduler_name:
            if len(os.sys.argv) > 1 and int(os.sys.argv[1]) > 0:
                # ensure previous job id finished before start this job
                prev_job_id = str(os.sys.argv[1])
                print(f'checking if previous job id = {prev_job_id} still is running')
                processes = str(subprocess.check_output('squeue -u $(id -un)', shell=True), 'utf')
                if prev_job_id in processes:
                    print(f'! previous job id = {prev_job_id} not finished - bailing!')
                    # make next job wait to avoid rapid string of restarts
                    # restart_time = time.strftime('%Y%m%d%H%M',
                    # time.localtime(time.time() + time_delay * 3600))
                    os.system(f'sbatch {file_name} {prev_job_id}')
                    exit()
                print('')
            elif submit_before:
                # submit next job, to wait for this one to finish
                os.system('sbatch {} {}'.format(file_name, os.environ['SLURM_JOB_ID']))

        elif 'pbs' in self.scheduler_name:
            if 'jobid' in os.environ and os.environ['jobid']:
                # ensure previous job id finished before start this job
                prev_job_id = os.environ['jobid']
                print(f'checking if previous job id = {prev_job_id} still is running')
                processes = str(subprocess.check_output('qstat -u $(id -un)', shell=True), 'utf')
                if prev_job_id in processes:
                    print(f'! previous job id = {prev_job_id} not finished - bailing!')
                    # make next job wait to avoid rapid string of restarts
                    restart_time = time.strftime(
                        '%Y%m%d%H%M', time.localtime(time.time() + time_delay * 3600)
                    )
                    os.system(f'qsub -v jobid={prev_job_id} -a {restart_time} {file_name}')
                    exit()
                print('')
            elif submit_before:
                # submit next job, to wait for this one to finish
                os.system('qsub -v jobid={} {}'.format(os.environ['PBS_JOBID'], file_name))

    def get_restart_flag(self, restart_from_snapshot=False):
        '''
        Parameters
        ----------
        restart_from_snapshot : bool
            whether to restart from snapshot file[s]

        Returns
        -------
        execute_command_restart_flag : str
            flag to add to executable
        '''
        from gizmo_analysis import gizmo_default

        restart_file_name_base = (
            gizmo_default.snapshot_directory
            + gizmo_default.restart_directory
            + gizmo_default.restart_file_name
        )
        execute_command_restart_flag = ''

        if restart_from_snapshot:
            execute_command_restart_flag = ' 2'
            print('restarting from snapshot file[s]\n')
        else:
            # check if restart files exist
            restart_file_names_tot = glob.glob(restart_file_name_base)

            if len(restart_file_names_tot) > 0:
                execute_command_restart_flag = ' 1'
                restart_file_names = [rfn for rfn in restart_file_names_tot if '.bak' not in rfn]
                restart_backup_file_names = [rfn for rfn in restart_file_names_tot if '.bak' in rfn]
                print(
                    'restarting from restart files: found {} regular, {} backup'.format(
                        len(restart_file_names), len(restart_backup_file_names)
                    )
                )
                if (
                    len(restart_file_names) != self.mpi_number
                    and len(restart_backup_file_names) != self.mpi_number
                ):
                    print(f'! number of restart files != number of MPI tasks = {self.mpi_number}')
                print('')

        return execute_command_restart_flag


# --------------------------------------------------------------------------------------------------
# paths and file names
# --------------------------------------------------------------------------------------------------
def get_path(directories, create_path=False, remove_period=False):
    '''
    Get path to directory[s], safely including trailing /.

    Parameters
    ----------
    directories : str or list thereof
        name[s] of directory[s]
    create_path : bool
        whether to create path if it does not exist
    remove_period : bool
        whether to remove preceding '.' of current directory

    Returns
    -------
    directories : str, or list of strings
    '''

    def get_path_single(directory, create_path, remove_period):
        if directory == '.' and remove_period:
            directory_return = ''
        elif directory[-1] != '/':
            directory_return = directory + '/'
        else:
            directory_return = directory

        if create_path:
            if not os.path.exists(directory_return):
                os.makedirs(directory_return)

        return directory_return

    if np.isscalar(directories):
        # single directory
        directories_return = get_path_single(directories, create_path, remove_period)
    else:
        # list of directories
        directories_return = list(directories)  # ensure is list
        for di, directory_return in enumerate(directories_return):
            directories_return[di] = get_path_single(directory_return, create_path, remove_period)

    return directories_return


def get_numbers_in_string(string, scalarize=False):
    '''
    Get list of int and float numbers in string.

    Parameters
    ----------
    string : str
    scalarize : bool
        whether to return scalar value if only one number

    Returns
    -------
    numbers : int[s] and/or float[s]
    '''
    numbers = []
    number = ''

    for ci, char in enumerate(string):
        if char.isdigit():
            number += char
        elif char == '.':
            if (
                number
                and ci > 0
                and string[ci - 1].isdigit()
                and len(string) > ci + 1
                and string[ci + 1].isdigit()
            ):
                number += char

        if number and ((not char.isdigit() and not char == '.') or ci == len(string) - 1):
            if '.' in number:
                numbers.append(float(number))
            else:
                numbers.append(int(number))
            number = ''

    if scalarize and len(numbers) == 1:
        numbers = numbers[0]

    return numbers


def get_file_names(file_name_base, number_type=None, sort_reverse=False, verbose=True):
    '''
    Get sorted list[s] of all file names (including full path) with given name base
    [and numbers in each file name, if number_type defined].

    Parameters
    ----------
    file_name_base : str
        base name of file, with full/relative path, using * as wildcard
    number_type : dtype
        type of number to get in file name (get final one of given type in name)
        options: None, int, float, (int, float), numbers.Real
    sort_reverse : bool
        whether to return list of file names and numbers in reverse order
    verbose : bool
        whether to print diagnostics

    Returns
    -------
    path_file_names : list of str
        names of files, with full path
    [file_numbers] : list of int and/or float
        numbers within each file name
    '''
    from gizmo_analysis import gizmo_default

    Say = SayClass(get_file_names)

    # get all file names matching string in directory
    path_file_names = glob.glob(file_name_base)
    if not path_file_names:
        Say.say(f'! cannot find files with base name:  {file_name_base}', verbose)
        if number_type:
            return [], []
        else:
            return path_file_names

    path_file_names.sort()

    # ignore snapshot time files
    for fn in list(path_file_names):
        if fn.endswith(gizmo_default.snapshot_time_file_name):
            path_file_names.remove(fn)
        if fn.endswith(gizmo_default.snapshot_scalefactor_file_name):
            path_file_names.remove(fn)

    if number_type is not None:
        # for a file name with numbers, get final number of given type in each file name
        file_numbers = []
        for path_file_name in path_file_names:
            file_name = path_file_name
            if '/' in file_name:
                file_name = file_name.split('/')[-1]
            if '.hdf5' in file_name:
                file_name = file_name.replace('.hdf5', '')

            file_numbers_t = get_numbers_in_string(file_name, scalarize=False)

            for file_number_t in reversed(file_numbers_t):
                if isinstance(file_number_t, number_type):
                    file_numbers.append(file_number_t)
                    break
            else:
                raise OSError(f'no number of type {number_type} in file: {path_file_name}')

        file_numbers = np.array(file_numbers)

        if sort_reverse:
            path_file_names = path_file_names[::-1]
            file_numbers = file_numbers[::-1]

        return path_file_names, file_numbers

    else:
        if sort_reverse:
            path_file_names = path_file_names[::-1]

        return path_file_names


def get_file_numbers_missing(
    file_name_base, number_min=0, number_max=None, sort_reverse=False, verbose=True
):
    '''
    Get sorted list[s] of all file numbers for file names that are missing,
    assuming file names with integer numbers from number_min to number_max.

    Parameters
    ----------
    file_name_base : str
        base name of file, with full/relative path, using * as wildcard
    number_min : int
        minimum file number expected
    number_max : int
        maximum file number expected
    sort_reverse : bool
        whether to return list of file names and numbers in reverse order
    verbose : bool
        whether to print diagnostics

    Returns
    -------
    path_file_names : list of str
        names of files, with full path
    file_numbers : list of int and/or float
        numbers within each file name
    '''
    Say = SayClass(get_file_numbers_missing)

    _path_file_names, file_numbers = get_file_names(file_name_base, int, verbose=verbose)

    if len(file_numbers) == 0:
        return []

    if number_min is None:
        number_min = np.min(file_numbers)
    if number_max is None:
        number_max = np.max(file_numbers)

    Say.say(
        f'checking for missing file numbers from {number_min} to {number_max}'
        + f' with name base = {file_name_base}'
    )

    file_numbers_all = np.arange(number_min, number_max + 1)
    file_numbers_missing = np.setdiff1d(file_numbers_all, file_numbers)

    if len(file_numbers_missing) == 0:
        Say.say('no missing file numbers')
    elif sort_reverse:
        file_numbers_missing = file_numbers_missing[::-1]

    return file_numbers_missing


def get_file_names_nearest_number(
    file_name_base,
    numbers=None,
    number_type=float,
    sort_kind=None,
    arrayize=False,
    dif_tolerance=0.1,
):
    '''
    Get sorted lists of file names (including full path) and numbers,
    whose number in its file name is closest to input number[s].

    Parameters
    ----------
    file_name_base : str
        base name of file, with full path, using * as wildcard
    numbers : float/int or list
        number[s] (such as scale-factors)
    number_type : dtype
        type of number in file name to get
        options: None, int, float
    sort_kind : str
        way to sort file names/numbers: None, 'forward', 'reverse'
    arrayize : bool
        whether to force return as array, even if single element
    dif_tolerance : float
        tolerance for warning flag in number rounding

    Returns
    -------
    file_names : list of str
        names of files, with full path
    file_numbers : list of int and/or float
        numbers within each file name
    '''
    if np.isscalar(numbers):
        numbers = [numbers]
    numbers = np.array(numbers)

    if sort_kind:
        numbers = np.sort(numbers)
        if sort_kind == 'reverse':
            numbers = numbers[::-1]

    # get all file names and numbers matching string in directory
    file_names_read, file_numbers_read = get_file_names(file_name_base, number_type)
    file_names = []
    file_numbers = []
    for number in numbers:
        number_difs = abs(number_type(number) - file_numbers_read)
        near_i = np.nanargmin(number_difs)
        # warn if number of file is too far from input value
        if number_difs[near_i] > dif_tolerance:
            print(
                f'! input number = {number}, but nearest file number = {file_numbers_read[near_i]}'
            )
        file_names.append(file_names_read[near_i])
        file_numbers.append(file_numbers_read[near_i])

    if numbers.size == 1 and not arrayize:
        # if input scalar number, return as scalar
        file_names = file_names[0]
        file_numbers = file_numbers[0]
    else:
        file_names, file_numbers = np.array(file_names), np.array(file_numbers)

    return file_names, file_numbers


def rename_files(directory, string_old='', string_new=''):
    '''
    For all file names containing string_old, rename string_old to string_old.

    Parameters
    ----------
    directory : str
    string_old : str
        file name to replace (can use *)
    string_new : str
        str with which to replace it (can also use *)
    '''
    directory = get_path(directory)
    file_names = glob.os.listdir(directory)

    if not file_names:
        print('found no files in directory: ' + directory)

    if '*' in string_old and '*' in string_new:
        strings_old = string_old.split('*')
        strings_new = string_new.split('*')
    else:
        strings_old = [string_old]
        strings_new = [string_new]

    if len(strings_old) != len(strings_new):
        raise ValueError(
            f'length of strings_old = {strings_old} not match strings_new = {strings_new}'
        )

    for file_name in file_names:
        file_name_new = file_name
        string_in_file = [False for string_old in strings_old]
        for si, string_old in enumerate(strings_old):
            if string_old in file_name:
                string_in_file[si] = True
                file_name_new = file_name_new.replace(string_old, strings_new[si])

        if np.min(string_in_file) and file_name_new != file_name:
            print('in', directory, 'rename', file_name, 'to', file_name_new)
            file_name = directory + file_name
            file_name_new = directory + file_name_new
            glob.os.rename(file_name, file_name_new)


# --------------------------------------------------------------------------------------------------
# read/write to/from file
# --------------------------------------------------------------------------------------------------
def file_hdf5(file_name_base, dict_or_array_to_write=None, verbose=True):
    '''
    Write or read to/from file in HDF5 format.
    Assumes data is numpy array[s] or dictionary thereof.

    Parameters
    ----------
    file_name_base : str
        base name for file (without '.hdf5')
    dict_or_array_to_write : any
        dictionary or single array to write
    verbose : bool
        whether to print each property read/written

    Returns
    -------
    [dict_read] : dict
        dictionary of dataset names + arrays
    '''
    Say = SayClass(file_hdf5)

    array_name_default = 'array'  # every HDF5 dataset needs a name

    if '.hdf5' not in file_name_base:
        file_name_base += '.hdf5'

    if dict_or_array_to_write is not None:
        # write to file
        if not isinstance(dict_or_array_to_write, dict):
            dict_out = {array_name_default: dict_or_array_to_write}
        else:
            dict_out = dict_or_array_to_write

        # create file
        with h5py.File(file_name_base, 'w') as file_out:
            Say.say('writing file:  {}'.format(file_name_base.lstrip('./')), verbose)

            for key in dict_out:
                if dict_out[key] is None:
                    continue

                key_use = key
                if '/' in key:
                    key_use = key_use.replace('/', '_div.by_')

                if dict_out[key].dtype == 'O':
                    # general numpy data type - assume is variable length array
                    for element in dict_out[key]:
                        if len(element) > 0:
                            dtype = h5py.special_dtype(vlen=element.dtype)
                            break
                    dset = file_out.create_dataset(key_use, (len(dict_out[key]),), dtype=dtype)
                    for ie, element in enumerate(dict_out[key]):
                        dset[ie] = element
                else:
                    file_out.create_dataset(key_use, data=dict_out[key])

                Say.say(
                    f'  {key_use} | {dict_out[key].dtype}, shape = {dict_out[key].shape}',
                    verbose,
                )
            print()

    else:
        # read from file
        with h5py.File(file_name_base, 'r') as file_in:
            Say.say('reading file:  {}'.format(file_name_base.lstrip('./')), verbose)
            # Say.say('reading file:  {}'.format(file_name_base.split('/')[-1]), verbose)

            dict_read = {}
            keys = list(file_in.keys())

            for key in keys:
                key_use = key
                if '_div.by_' in key:
                    key_use = key_use.replace('_div.by_', '/')

                dict_read[key_use] = np.array(file_in.get(key))

                Say.say(
                    f'  {key} | {dict_read[key_use].dtype}, shape = {dict_read[key_use].shape}',
                    verbose,
                )

        return dict_read


def file_pickle(file_name, object_to_write=None, protocol=None):
    '''
    Write or read to/from file in pickle format.

    Parameters
    ----------
    file_name : str
        name of file (without '.pkl')
    object_to_write : any
        object to write
    protocal : int
        pickle protocal (file type) to use. 2 = compatible with Python 2.3+

    Returns
    -------
    [obj] : python object
    '''
    import pickle

    Say = SayClass(file_pickle)

    if '.pkl' not in file_name:
        file_name += '.pkl'

    if object_to_write is not None:
        # write to file
        with open(file_name, 'wb') as file_out:
            pickle.dump(object_to_write, file_out, protocol)

        Say.say(f'wrote file:  {file_name}')

    else:
        # read from file
        with open(file_name, 'rb') as file_in:
            obj = pickle.load(file_in)

        Say.say('read file:  {}\n'.format(file_name.split('/')[-1]))

        return obj


# --------------------------------------------------------------------------------------------------
# run function in parallel
# --------------------------------------------------------------------------------------------------
def run_in_parallel(func, args_list, kwargs={}, proc_number=1, verbose=False):
    '''
    Run function in parallel, looping over inputs.
    ADD: example

    Parameters
    ----------
    func : function object
    args_list : list
        list of arguments to func, with one bundle per parallelized iteration
    kwargs : dict
        keyword arguments to send to the function (same for all iterations)
    proc_number : int
        number of parallel processes to use
    verbose : bool
        whether to print name of function and its inputs
    '''
    if proc_number > len(args_list):
        proc_number = len(args_list)  # threads <= input argument combinations

    if proc_number > 1:
        from multiprocessing import Pool

        pool = Pool(proc_number)
        for args in args_list:
            if verbose:
                print_flush(f'running in parallel:  {func.__name__}{args}')
            pool.apply_async(func, args, kwargs)
        pool.close()
        pool.join()

        # this method appears slower, and 'with Pool' does not appear to work with *_async()
        # with Pool(proc_number) as pool:
        #    if verbose:
        #        for args in args_list:
        #            print_flush('running in parallel:  {}{}'.format(func.__name__, args))
        #    pool.starmap(func, args_list)

    else:
        for args in args_list:
            if verbose:
                print_flush(f'running in serial:  {func.__name__}{args}')
            func(*args, **kwargs)
