use std::os::raw::c_char;
use std::ffi::CStr;

#[no_mangle]
fn alignment(first: *const c_char, second: *const c_char) -> u32 {
    
    let first_sequence = unsafe {
        assert!(!first.is_null());
        CStr::from_ptr(first)
    };
    let second_sequence = unsafe {
        assert!(!second.is_null());
        CStr::from_ptr(second)
    };
    let first_string = first_sequence.to_str().unwrap();
    let second_string = second_sequence.to_str().unwrap();
    
    
    return 8
}
