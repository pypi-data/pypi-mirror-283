"""
Test basic conversion functions.
"""
import pytest

from bh_utils.conversions import (
    str_to_bool,
    is_integer,
)

@pytest.mark.conversions
def test_str_to_bool_valid_01():
    res = str_to_bool( 'true' )
    assert res == True

    res = str_to_bool( '1' )
    assert res == True

    res = str_to_bool( 't' )
    assert res == True

    res = str_to_bool( 'yes' )
    assert res == True

    res = str_to_bool( 'y' )
    assert res == True

    res = str_to_bool( 'on' )
    assert res == True

    res = str_to_bool( 'false' )
    assert res == False

    res = str_to_bool( '0' )
    assert res == False    
    
    res = str_to_bool( 'f' )
    assert res == False    
    
    res = str_to_bool( 'no' )
    assert res == False    
    
    res = str_to_bool( 'n' )
    assert res == False    
    
    res = str_to_bool( 'off' )
    assert res == False    

@pytest.mark.conversions
def test_str_to_bool_valid_02():
    res = str_to_bool( 'False', '"False" is not a valid Boolean value' )
    assert res == False

@pytest.mark.conversions
def test_str_to_bool_invalid():
    res = str_to_bool( 'accept' )
    assert res == None

    exception_msg = 'Invalid Boolean value...'
    res == None
    exception_msg_raised = ''
    try:
        res = str_to_bool( 'accept', exception_msg )
    except Exception as e:
        exception_msg_raised = str( e )

    assert res == None
    assert exception_msg_raised == exception_msg
	
@pytest.mark.conversions
def test_is_integer_01():
    x = 9
    res = is_integer( x )
    assert res == True
	
    x = '9'
    res = is_integer( x )
    assert res == True

    x = 9.05
    res = is_integer( x )
    assert res == False

    x = '9.05'
    res = is_integer( x )
    assert res == False

    x = None
    res = is_integer( x )
    assert res == False

    x = 'ab1'
    res = is_integer( x )
    assert res == False
	
@pytest.mark.conversions
def test_is_integer_02():
    class BHInt( int ):
        pass

    x = BHInt()	
    assert x != None

    x = 10
    res = is_integer( x )
    assert res == True

@pytest.mark.conversions
def test_is_integer_03():
    class BHStr( str ):
        pass

    x = BHStr()	
    assert x != None

    x = '10'
    res = is_integer( x )
    assert res == True
	
    x = '10.0'
    res = is_integer( x )
    assert res == False
	
    x = 'xx'
    res = is_integer( x )
    assert res == False
	
@pytest.mark.conversions
def test_is_integer_04():
    class BHStr( str ):
        pass

    x = BHStr()	
    assert x != None

    x = '10'
    res = is_integer( x )
    assert res == True
	
    x = '10.0'
    res = is_integer( x )
    assert res == False
	
    x = 'xx'
    res = is_integer( x )
    assert res == False	
	
@pytest.mark.conversions
def test_is_integer_05():
    class Test:
        def __init__( self, n: int ):
            self.__n = n
        @property
        def n( self ): return self.__n

    x = Test( 6 )	
    assert x != None
    assert x.n == 6
    res = is_integer( x )
    assert res == False