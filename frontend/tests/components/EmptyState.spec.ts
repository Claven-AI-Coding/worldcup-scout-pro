import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import EmptyState from '@/components/common/EmptyState.vue'

describe('EmptyState', () => {
  it('renders with default props', () => {
    const wrapper = mount(EmptyState)
    expect(wrapper.exists()).toBe(true)
  })

  it('displays custom message', () => {
    const message = 'No data available'
    const wrapper = mount(EmptyState, {
      props: { message },
    })
    expect(wrapper.text()).toContain(message)
  })

  it('displays custom description', () => {
    const description = 'Try again later'
    const wrapper = mount(EmptyState, {
      props: { description },
    })
    expect(wrapper.text()).toContain(description)
  })

  it('renders icon based on type', () => {
    const wrapper = mount(EmptyState, {
      props: { type: 'search' },
    })
    const svg = wrapper.find('svg')
    expect(svg.exists()).toBe(true)
  })

  it('emits action event when button clicked', async () => {
    const wrapper = mount(EmptyState, {
      props: {
        actionText: 'Retry',
      },
    })
    const button = wrapper.find('button')
    await button.trigger('click')
    expect(wrapper.emitted('action')).toBeTruthy()
  })
})
